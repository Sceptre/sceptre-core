from unittest.mock import patch
from sceptre.file_manager import FileManager


class TestFileManager:

    @patch('sceptre.context.SceptreContext')
    def test_get_all_stacks_as_map(self, mock_context, fs):
        baseconfig = """---
region: eu-west-1
template_path: templates/vpc.json

"""
        config_a = """---
profile: dev
map:
    1: 2
list:
    - a
    - b
"""

        config_b = """---
region: us-east-2
map:
    3: 4
    5: 6
list:
    - c
    - d
"""

        stack_a = """---
itemA: value_a
"""
        stack_b = """---
itemB: value_b
"""
        fs.create_file('/var/data/config/config.yaml', contents=baseconfig)
        fs.create_file('/var/data/config/stack.yaml', contents=stack_a)
        fs.create_file('/var/data/config/stack_b.yaml', contents=stack_a)
        fs.create_file('/var/data/config/b/stack.yaml', contents=stack_a)
        fs.create_file('/var/data/config/c/stack.yaml', contents=stack_b)
        fs.create_file('/var/data/config/c/config.yaml', contents=config_a)
        fs.create_file('/var/data/config/c/d/e/stack.yaml', contents=stack_a)
        fs.create_file('/var/data/config/c/d/e/config.yaml', contents=config_b)

        mock_context.full_command_path = '/var/data/config'
        mock_context.full_config_path = '/var/data/config'
        mock_context.config_path = 'config.yaml'
        fm = FileManager(mock_context)

        assert fm.all_stacks == {
            "/var/data/config/stack.yaml": {
                'itemA': 'value_a',
                'stack_config': {
                    "region": "eu-west-1",
                    'template_path': 'templates/vpc.json',
                }
            },
            "/var/data/config/stack_b.yaml": {
                'itemA': 'value_a',
                'stack_config': {
                    "region": "eu-west-1",
                    'template_path': 'templates/vpc.json',
                }
            },
            "/var/data/config/b/stack.yaml": {
                'itemA': 'value_a',
                'stack_config': {
                    "region": "eu-west-1",
                    "template_path": 'templates/vpc.json'
                }
            },
            "/var/data/config/c/stack.yaml": {
                'itemB': 'value_b',
                'stack_config': {
                    'map': {1: 2, 3: 4, 5: 6},
                    'list': ['c', 'd', 'a', 'b'],
                    'region': 'us-east-2',
                    'profile': 'dev',
                    'template_path': 'templates/vpc.json',

                }
            },
            "/var/data/config/c/d/e/stack.yaml": {
                'itemA': 'value_a',
                'stack_config': {
                    'map': {3: 4, 5: 6},
                    'list': ['c', 'd'],
                    'region': 'us-east-2',
                    'template_path': 'templates/vpc.json',
                }
            }
        }

    @patch('sceptre.context.SceptreContext')
    def test_get_command_stacks_as_map(self, mock_context, fs):
        baseconfig = """---
region: eu-west-1
template_path: templates/vpc.json

"""
        config_a = """---
profile: dev
map:
    1: 2
list:
    - a
    - b
"""

        config_b = """---
region: us-east-2
map:
    3: 4
    5: 6
list:
    - c
    - d
"""

        stack_a = """---
itemA: value_a
"""
        stack_b = """---
itemB: value_b
"""
        fs.create_file('/var/data/config/config.yaml', contents=baseconfig)
        fs.create_file('/var/data/config/stack.yaml', contents=stack_a)
        fs.create_file('/var/data/config/stack_b.yaml', contents=stack_a)
        fs.create_file('/var/data/config/b/stack.yaml', contents=stack_a)
        fs.create_file('/var/data/config/c/stack.yaml', contents=stack_b)
        fs.create_file('/var/data/config/c/config.yaml', contents=config_a)
        fs.create_file('/var/data/config/c/d/e/stack.yaml', contents=stack_a)
        fs.create_file('/var/data/config/c/d/e/config.yaml', contents=config_b)

        mock_context.full_command_path = '/var/data/config/c'
        mock_context.full_config_path = '/var/data/config'
        mock_context.config_path = 'config.yaml'
        fm = FileManager(mock_context)

        assert fm.command_stacks == {
            "/var/data/config/c/stack.yaml": {
                'itemB': 'value_b',
                'stack_config': {
                    'map': {1: 2, 3: 4, 5: 6},
                    'list': ['c', 'd', 'a', 'b'],
                    'region': 'us-east-2',
                    'profile': 'dev',
                    'template_path': 'templates/vpc.json',

                }
            },
            "/var/data/config/c/d/e/stack.yaml": {
                'itemA': 'value_a',
                'stack_config': {
                    'map': {3: 4, 5: 6},
                    'list': ['c', 'd'],
                    'region': 'us-east-2',
                    'template_path': 'templates/vpc.json',
                }
            }
        }

        assert len(fm.all_stacks) == 5
        assert len(fm.command_stacks) == 2

    @patch('sceptre.context.SceptreContext')
    def test_get_single_command_stacks_as_map(self, mock_context, fs):
        baseconfig = """---
region: eu-west-1
template_path: templates/vpc.json

"""
        config_a = """---
profile: dev
map:
    1: 2
list:
    - a
    - b
"""

        config_b = """---
region: us-east-2
map:
    3: 4
    5: 6
list:
    - c
    - d
"""

        stack_a = """---
itemA: value_a
"""
        stack_b = """---
itemB: value_b
"""
        fs.create_file('/var/data/config/config.yaml', contents=baseconfig)
        fs.create_file('/var/data/config/stack.yaml', contents=stack_a)
        fs.create_file('/var/data/config/stack_b.yaml', contents=stack_a)
        fs.create_file('/var/data/config/b/stack.yaml', contents=stack_a)
        fs.create_file('/var/data/config/c/stack.yaml', contents=stack_b)
        fs.create_file('/var/data/config/c/config.yaml', contents=config_a)
        fs.create_file('/var/data/config/c/d/e/stack.yaml', contents=stack_a)
        fs.create_file('/var/data/config/c/d/e/config.yaml', contents=config_b)

        mock_context.full_command_path = '/var/data/config/c/d/e'
        mock_context.full_config_path = '/var/data/config'
        mock_context.config_path = 'config.yaml'
        fm = FileManager(mock_context)

        assert fm.command_stacks == {
            "/var/data/config/c/d/e/stack.yaml": {
                'itemA': 'value_a',
                'stack_config': {
                    'map': {3: 4, 5: 6},
                    'list': ['c', 'd'],
                    'region': 'us-east-2',
                    'template_path': 'templates/vpc.json',
                }
            }
        }

        assert len(fm.all_stacks) == 5
        assert len(fm.command_stacks) == 1
