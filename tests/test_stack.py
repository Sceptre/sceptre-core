import pytest

from sceptre.providers.stack import StackConfigData
from sceptre.providers.stack import Stack


class TestStack(object):
    def test_stack_instantiates_correctly_with_stack_config_data(self):
        stack_config = StackConfigData(name="hello")
        stack = Stack(stack_config)
        assert stack.config == stack_config

    def test_stack_raises_type_error_when_instantiated_without_stack_config_data(self):
        bad_config = {}
        with pytest.raises(TypeError):
            Stack(bad_config)


class TestStackConfigData(object):
    def test_stack_config_data_dict_accessible_with_dot_notation(self):
        stack_config = StackConfigData(name="hello")
        assert stack_config.name == "hello"

    def test_stack_config_missing_attr_raises_attribute_error(self):
        stack_config = StackConfigData(name="hello")
        with pytest.raises(AttributeError):
            stack_config.region == "hello"

    def test_stack_config_delete_attr_raises_attribute_error(self):
        stack_config = StackConfigData(name="hello")
        assert stack_config.name == "hello"
        with pytest.raises(AttributeError):
            del(stack_config.region)

    def test_stack_config_delete_attr_correctly_removes_attr(self):
        stack_config = StackConfigData(name="hello")
        assert stack_config.name == "hello"
        del(stack_config.name)
        with pytest.raises(AttributeError):
            stack_config.name
