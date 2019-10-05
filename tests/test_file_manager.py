from mock import patch
from sceptre.file_manager import FileManager


class TestFileManager(object):

    @patch('sceptre.context.SceptreContext')
    def test_get_all_stacks_as_file_data(self, mock_context, fs):
        baseconfig = """---
region: eu-west-1
template_path: templates/vpc.json

"""
        configA = """---
profile: dev
map:
    1: 2
list:
    - a
    - b
"""

        configB = """---
region: us-east-2
map:
    3: 4
    5: 6
list:
    - c
    - d
"""

        stackA = """---
itemA: valueA
"""
        stackB = """---
itemB: valueB
"""
        fs.create_file('/var/data/config/config.yaml', contents=baseconfig)
        fs.create_file('/var/data/config/stack.yaml', contents=stackA)
        fs.create_file('/var/data/config/stackB.yaml', contents=stackA)
        fs.create_file('/var/data/config/b/stack.yaml', contents=stackA)
        fs.create_file('/var/data/config/c/stack.yaml', contents=stackB)
        fs.create_file('/var/data/config/c/config.yaml', contents=configA)
        fs.create_file('/var/data/config/c/d/e/stack.yaml', contents=stackA)
        fs.create_file('/var/data/config/c/d/e/config.yaml', contents=configB)

        mock_context.full_command_path = '/var/data/config'
        mock_context.full_config_path = '/var/data/config'
        mock_context.config_path = 'config.yaml'
        fm = FileManager(mock_context)

        assert fm.all_stacks == {
            "/var/data/config/stack.yaml": {
                'itemA': 'valueA',
                'stack_config': {
                    "region": "eu-west-1",
                    'template_path': 'templates/vpc.json',
                }
            },
            "/var/data/config/stackB.yaml": {
                'itemA': 'valueA',
                'stack_config': {
                    "region": "eu-west-1",
                    'template_path': 'templates/vpc.json',
                }
            },
            "/var/data/config/b/stack.yaml": {
                'itemA': 'valueA',
                'stack_config': {
                    "region": "eu-west-1",
                    "template_path": 'templates/vpc.json'
                }
            },
            "/var/data/config/c/stack.yaml": {
                'itemB': 'valueB',
                'stack_config': {
                    'map': {1: 2, 3: 4, 5: 6},
                    'list': ['c', 'd', 'a', 'b'],
                    'region': 'us-east-2',
                    'profile': 'dev',
                    'template_path': 'templates/vpc.json',

                }
            },
            "/var/data/config/c/d/e/stack.yaml": {
                'itemA': 'valueA',
                'stack_config': {
                    'map': {3: 4, 5: 6},
                    'list': ['c', 'd'],
                    'region': 'us-east-2',
                    'template_path': 'templates/vpc.json',
                }
            }
        }
