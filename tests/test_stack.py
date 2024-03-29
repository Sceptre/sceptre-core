import pytest

from sceptre.provider.stack import StackConfigData
from sceptre.provider.stack import Stack


class TestStack:

    def test_stack_instantiates_correctly_with_stack_config_data(self, stack_config, provider):
        stack = Stack("/var/a/b/c.yaml", stack_config)
        assert stack.config == stack_config

    def test_stack_raises_type_error_when_instantiated_without_stack_config_data(self):
        bad_config = {}
        with pytest.raises(TypeError):
            Stack("/var/a/b/c.yaml", bad_config)

    def test_stack_instantiates_with_hashed_id(self, stack_config, provider):
        stack = Stack("/var/a/b/c/d.yaml", stack_config)
        assert stack.id == "/var/a/b/c/d.yaml"


class TestStackConfigData:
    def test_stack_config_data_dict_accessible_with_dot_notation(self):
        stack_config = StackConfigData({"name": "hello"})
        assert stack_config.name == "hello"

    def test_stack_config_missing_attr_raises_attribute_error(self):
        stack_config = StackConfigData(name="hello")
        assert stack_config.region is None

    def test_stack_config_delete_attr_raises_attribute_error(self):
        stack_config = StackConfigData(name="hello")
        assert stack_config.name == "hello"
        with pytest.raises(AttributeError):
            del(stack_config.region)

    def test_stack_config_delete_attr_correctly_removes_attr(self):
        stack_config = StackConfigData(name="hello")
        assert stack_config.name == "hello"
        del(stack_config.name)
        stack_config.name is None
