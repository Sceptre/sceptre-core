import pytest
from mock import patch

from sceptre.exceptions import SceptreYamlError

from sceptre.file_manager.file_handler import FileHandler
from sceptre.file_manager.file_handler import FileData


class TestFileHandler(object):
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

    def test_valid_yaml_file_parses_successfully(self, tmpdir):
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

    @patch('resolver.environment_variable.EnvironmentVariable')
    def test_valid_yaml_file_parses_successfully_custom_tags(self, mock_env_resolver, tmpdir):
        mock_env_resolver.return_value = 'env_var'
        path = tmpdir.mkdir("dummy_path").join('stack.yaml')
        stream = """---
keyA: !environment_variable env_var
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