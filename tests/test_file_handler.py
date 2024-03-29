import pytest
from unittest.mock import patch

from sceptre.exceptions import SceptreYamlError

from sceptre.file_manager.file_handler import FileHandler
from sceptre.file_manager.file_handler import FileData


class TestFileHandler:
    def setup_method(self):
        self.fh = FileHandler()

    @patch('sceptre.file_manager.file_data.FileData')
    def test_file_opens_with_valid_path(self, mock_file_data, tmpdir):
        path = tmpdir.mkdir("dummy_path").join("test.yaml")
        path.write("hello")
        fd_path = mock_file_data.path = path
        fd_stream = mock_file_data.stream = 'hello'
        f = self.fh.open(path)
        assert mock_file_data.called_once_with(path, 'hello')
        assert f.path == fd_path
        assert f.stream == fd_stream

    def test_file_open_raises_file_not_found_error(self):
        with pytest.raises(FileNotFoundError):
            self.fh.open('no_file.yaml')

    def test_valid_simple_yaml_file_parses(self, tmpdir):
        path = tmpdir.mkdir("dummy_path").join('stack.yaml')
        stream = """---
keyA: valueA
listB:
  - itemA
  - itemB
  - itemC
"""
        path.write(stream)
        fd = FileData(path, stream)
        parsed = self.fh.parse(fd)
        assert parsed.stream == {
            'keyA': 'valueA',
            'listB': ['itemA', 'itemB', 'itemC']
        }

    @patch('resolver.test_resolver_fixture.TestResolver')
    def test_valid_yaml_file_parses_custom_yaml_tags(self, mock_resolver, tmpdir):
        mock_resolver.return_value = 'env_var'
        path = tmpdir.mkdir("dummy_path").join('stack.yaml')
        stream = """---
keyA: !test_resolver_fixture
listB:
  - itemA
  - itemB
  - itemC
"""
        path.write(stream)
        fd = FileData(path, stream)
        parsed = self.fh.parse(fd)
        assert parsed.stream == {
            'keyA': 'env_var',
            'listB': ['itemA', 'itemB', 'itemC']
        }

    @patch('sceptre.file_manager.file_data.FileData')
    def test_invalid_yaml_file_raises_parse_error(self, mock_file_data):
        mock_file_data.path = 'path/to/file.yaml'
        mock_file_data.stream = """
>>>>
keyA: valueA
"""
        with pytest.raises(SceptreYamlError):
            self.fh.parse(mock_file_data)
            assert mock_file_data.called_once()

    @patch('sceptre.context.SceptreContext')
    def test_render_succesfully_renders_vars(self, mock_context, tmpdir):
        mock_context.user_variables = {"test_var": "resolvedVariable"}
        mock_context.command_path = "a/b/"
        variables = {
            "var": mock_context.user_variables,
            "stack_config": {},
            "command_path": mock_context.command_path
        }
        path = tmpdir.mkdir("dummy_path").join('stack.yaml')
        stream = """---
keyA: valueA
listB:
  - {{ var.test_var }}
  - itemB
  - itemC
"""
        path.write(stream)
        fd = FileData(path, stream)
        rendered = self.fh.render(fd, variables=variables)
        parsed = self.fh.parse(rendered)
        assert parsed.stream == {
            'keyA': 'valueA',
            'listB': ['resolvedVariable', 'itemB', 'itemC']
        }

    @patch('sceptre.context.SceptreContext')
    def test_render_succesfully_renders_command_path(self, mock_context, tmpdir):
        mock_context.command_path = "command/path/stack.yaml"
        path = tmpdir.mkdir("dummy_path").join('stack.yaml')
        stream = """---
keyA: {{ command_path.0 }}
listB:
  - {{ command_path.1 }}
  - itemB
  - itemC
"""
        path.write(stream)
        fd = FileData(path, stream)
        rendered = self.fh.render(fd, {"command_path": mock_context.command_path})
        parsed = self.fh.parse(rendered)
        assert parsed.stream == {
            'keyA': 'command',
            'listB': ['path', 'itemB', 'itemC']
        }

    @patch('sceptre.context.SceptreContext')
    def test_render_succesfully_render_stack_config(self, mock_context, tmpdir):
        mock_context.command_path = "command/path/stack.yaml"
        path = tmpdir.mkdir("dummy_path").join('stack.yaml')
        stream = """---
keyA: {{ stack_config.region }}
listB:
  - itemB
  - itemC
"""
        path.write(stream)
        fd = FileData(path, stream)
        rendered = self.fh.render(fd, {
            "var": {},
            "stack_config": {"region": "eu-west-1"},
            "command_path": mock_context.command_path
        }
        )
        parsed = self.fh.parse(rendered)
        assert parsed.stream == {
            'keyA': 'eu-west-1',
            'listB': ['itemB', 'itemC']
        }
