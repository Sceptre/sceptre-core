from mock import patch
from sceptre.file_manager import FileManager


class TestFileManager(object):

    @patch('sceptre.context.SceptreContext')
    def test_get_all_stacks_as_file_data(self, mock_context, fs):
        config = {"region": "eu-west-1"}
        stackA = """---
itemA: valueA
"""
        stackB = """---
itemB: valueB
"""
        fs.create_file('/var/data/config/config.yaml', contents=config)
        fs.create_file('/var/data/config/b/stack.yaml', contents=stackA)
        fs.create_file('/var/data/config/c/stack.yaml', contents=stackB)
        fs.create_file('/var/data/config/c/d/e/stack.yaml', contents=stackA)

        mock_context.full_command_path = '/var/data/config'
        fm = FileManager(mock_context)

        assert fm.all_stacks == {
            "/var/data/config/b/stack.yaml": {'itemA': 'valueA'},
            "/var/data/config/c/stack.yaml": {'itemB': 'valueB'},
            "/var/data/config/c/d/e/stack.yaml": {'itemA': 'valueA'}
        }
