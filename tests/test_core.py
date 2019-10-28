import pytest

from sceptre.core import SceptreCore
from sceptre.provider.stack import Stack


@pytest.fixture()
def stack_map():
    stack_map = {
        "/var/data/config/stack.yaml": {
            "name": "Stack1",
            "region": "eu-west-1",
            'template_path': 'templates/vpc.json',
            'dependencies': '/var/data/config/stack_b.yaml'
        },
        "/var/data/config/stack_b.yaml": {
            "name": "Stack2",
            "region": "eu-west-2",
            'template_path': 'templates/vpc.json',
        },
    }
    return stack_map


class TestCore:
    def test_core_instantiation_generates_stacks(self, stack_map):
        core = SceptreCore(stack_map)
        assert len(core.stacks) == 2

    def test_core_stack_list_contains_stacks(self, stack_map):
        core = SceptreCore(stack_map)
        assert isinstance(core.stacks.pop(), Stack)

    def test_stacks_are_added_to_graph(self, stack_map):
        core = SceptreCore(stack_map)
        assert len(core.graph) == len(stack_map)

    def test_stack_dependencies_are_correct(self, stack_map):
        core = SceptreCore(stack_map)
        for a, b in core.graph.graph.edges:
            assert a.id == '/var/data/config/stack_b.yaml' \
                and b.id == '/var/data/config/stack.yaml'
