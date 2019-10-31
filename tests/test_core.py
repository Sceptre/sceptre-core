import pytest

from sceptre.exceptions import ConfigFileNotFoundError
from sceptre.exceptions import ProviderNotFoundError
from sceptre.core import SceptreCore
from sceptre.context import SceptreContext
from sceptre.provider.stack import Stack
from sceptre.provider import Command


@pytest.fixture()
def create_stack_command(provider):
    class CreateStack(Command, provider=provider):

        def execute(cls):
            return "create_command executed"
    return CreateStack


@pytest.fixture()
def pattern():
    return "/var/data/config/stack"


@pytest.fixture()
def stack_map():
    stack_map = {
        "/var/data/config/stack.yaml": {
            "provider": "A",
            "name": "Stack1",
            "region": "eu-west-1",
            'template_path': 'templates/vpc.json',
            'dependencies': '/var/data/config/stack_b.yaml'
        },
        "/var/data/config/stack_b.yaml": {
            "provider": "A",
            "name": "Stack2",
            "region": "eu-west-2",
            'template_path': 'templates/vpc.json',
        },
        "/var/data/config/another/stack_b.yaml": {
            "provider": "A",
            "name": "Stack2",
            "region": "eu-west-2",
            'template_path': 'templates/vpc.json',
        },

    }
    return stack_map


@pytest.fixture(scope='function')
def sceptre_context():
    return SceptreContext("/var/data/config", "another/stack_b.yaml", ignore_dependencies=False)


class TestCore:
    def test_core_instantiation_generates_stacks(self, stack_map,
                                                 pattern, sceptre_context, provider):
        core = SceptreCore(stack_map, pattern, sceptre_context)
        assert len(core.stacks) == len(stack_map)

    def test_core_stack_list_contains_stacks(self, stack_map, pattern, sceptre_context, provider):
        core = SceptreCore(stack_map, pattern, sceptre_context)
        assert isinstance(core.stacks.pop(), Stack)

    def test_stacks_are_added_to_graph(self, stack_map, pattern, sceptre_context, provider):
        core = SceptreCore(stack_map, pattern, sceptre_context)
        assert len(core.graph) == len(stack_map)

    def test_stack_dependencies_are_correct(self, stack_map, pattern, sceptre_context, provider):
        core = SceptreCore(stack_map, pattern, sceptre_context)
        for a, b in core.graph.graph.edges:
            assert a.id == '/var/data/config/stack_b.yaml' \
                and b.id == '/var/data/config/stack.yaml'

    def test_execute_stacks_filter_correctly_on_pattern(self, stack_map, pattern,
                                                        sceptre_context, provider):
        core = SceptreCore(stack_map, pattern, sceptre_context)
        assert len(core.execute_stacks) == 2

    def test_execute_order_with_ignore_dependencies_returns_single_stack(self,
                                                                         stack_map,
                                                                         sceptre_context,
                                                                         provider):
        pattern = "/var/data/config/stack.yaml"
        sceptre_context.ignore_dependencies = True
        core = SceptreCore(stack_map, pattern, sceptre_context)
        stack = core.execute_order[0].pop()
        assert stack.id == "/var/data/config/stack.yaml"

    def test_execute_order_with_all_stacks_returns_two_batches(self, stack_map,
                                                               sceptre_context, provider):
        pattern = "/var/data/config"
        core = SceptreCore(stack_map, pattern, sceptre_context)
        assert len(core.execute_order[0]) == 2 and len(core.execute_order[1]) == 1

    def test_incorrect_pattern_name_raises_exception(self, stack_map, sceptre_context, provider):
        pattern = "non-existant-pattern.yaml"
        with pytest.raises(ConfigFileNotFoundError):
            SceptreCore(stack_map, pattern, sceptre_context)

    def test_provider_not_found_error_raised_with_missing_provider(self, sceptre_context):
        pattern = "/var/data/config/stack.yaml"
        stack_config = {
            "/var/data/config/stack.yaml": {
                "provider": "Hello",
                "name": "Stack1",
                "region": "eu-west-1",
                'template_path': 'templates/vpc.json',
            }
        }

        with pytest.raises(ProviderNotFoundError):
            SceptreCore(stack_config, pattern, sceptre_context)

    def test_command_is_executed(self, stack_map, sceptre_context, provider, create_stack_command):
        pattern = "/var/data/config/stack_b.yaml"
        core = SceptreCore(stack_map, pattern, sceptre_context)
        result = core.execute("create_stack")
        for k, v in result.items():
            assert v == "create_command executed"
