import pytest

from sceptre.provider import Command


@pytest.fixture
def create_stack_command(provider):
    class CreateStack(Command, provider=provider):
        def execute(cls):
            pass
    return CreateStack


@pytest.fixture
def update_change_command(provider):
    class UpdateChange(Command, provider=provider):
        def execute(cls):
            pass
    return UpdateChange


class TestProviderCommand:
    def test_provider_command_registers_sub_class(self, provider, create_stack_command):
        assert create_stack_command == provider.command_registry['create']['create_stack']

    def test_provider_command_raises_exception_when_provider_is_none(self):
        with pytest.raises(TypeError):
            class CreateStack(Command, provider=None):
                def execute(cls):
                    pass

    def test_update_command_registers_with_update_key(self, provider, update_change_command):
        assert update_change_command == provider.command_registry['update']['update_change']
