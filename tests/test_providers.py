import pytest

from sceptre.exceptions import DuplicateProviderRegistrationError
from sceptre.providers import ProviderRegistry
from sceptre.providers.schema import ProviderSchema
from sceptre.providers import Provider
from sceptre.providers.connection_manager import ConnectionManager


class TestProvider(object):
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
        assert isinstance(provider.schema, ProviderSchema)

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


class TestProviderRegistry(object):
    def test_registry_automatically_registers_subclass(self, schema,
                                                       connection_manager,
                                                       provider):
        assert ProviderRegistry.registry()["A"] == provider.__class__

    def test_registry_raises_duplication_error_on_same_provider(self, schema,
                                                                connection_manager, provider):
        with pytest.raises(DuplicateProviderRegistrationError):
            ProviderRegistry.register(provider, 'a')
            ProviderRegistry.register(provider, 'a')
