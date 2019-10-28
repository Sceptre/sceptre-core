import pytest

from sceptre.core import SceptreCore
from sceptre.provider.stack import Stack


@pytest.fixture()
def stack_map():
    stack_map = {
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
                "region": "eu-west-2",
                'template_path': 'templates/vpc.json',
            }
        },
    }
    return stack_map


class TestCore:
    def test_core_instantiation_generates_stacks(self, stack_map):
        core = SceptreCore(stack_map)
        assert len(core.stacks) == 2

    def test_core_stack_list_contains_stacks(self, stack_map):
        core = SceptreCore(stack_map)
        assert isinstance(core.stacks[0], Stack)
