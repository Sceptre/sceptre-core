import pytest

from sceptre.exceptions import DuplicateProviderRegistrationError
from sceptre.provider import ProviderRegistry
from sceptre.provider.schema import SchemaInterface
from sceptre.provider import Provider
from sceptre.provider.connection_manager import ConnectionManager


class TestProvider:
    def test_provider_instantiates_with_provider_name(
            self, schema, connection_manager
    ):
        provider = Provider('A', schema, connection_manager)
        assert provider.name == 'A'

    def test_provider_raises_value_error_if_provider_name_is_none(
            self, schema, provider
    ):
        connection_manager = {}
        with pytest.raises(ValueError):
            Provider(None, schema, connection_manager)

    def test_provider_instantiates_with_correct_schema_type(
            self, schema, connection_manager, provider
    ):

        provider = Provider('C', schema, connection_manager)
        assert isinstance(provider.schema, SchemaInterface)

    def test_provider_instantiates_with_correct_connection_manager_type(
            self, schema, connection_manager
    ):
        provider = Provider('D', schema, connection_manager)
        assert isinstance(provider.connection_manager, ConnectionManager)

    def test_provider_raises_type_error_with_incorrect_connection_manager_property_type(
            self, schema
    ):
        connection_manager = {}
        with pytest.raises(TypeError):
            Provider('E', schema, connection_manager)

    def test_provider_raises_type_error_incorrect_schema_property_type(self, connection_manager):
        schema = {}
        with pytest.raises(TypeError):
            Provider('F', schema, connection_manager)


class TestProviderRegistry:
    def test_registry_automatically_registers_subclass(self, schema,
                                                       connection_manager,
                                                       provider):
        assert ProviderRegistry.registry()["A"] == provider.__class__

    def test_registry_raises_duplication_error_on_same_provider(self, schema,
                                                                connection_manager, provider):
        with pytest.raises(DuplicateProviderRegistrationError):
            ProviderRegistry.register(provider, 'a')
            ProviderRegistry.register(provider, 'a')

    def test_external_provider_registers_successfully(self):
        ProviderRegistry.add_external_providers()
        assert "provider_test_fixture" in ProviderRegistry.registry()
