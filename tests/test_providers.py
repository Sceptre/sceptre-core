import pytest
from unittest import mock

from sceptre.providers import ProviderRegistry
from sceptre.providers.schema import ProviderSchema, Schema
from sceptre.providers import Provider
from sceptre.providers.connection_manager import ConnectionManager


@pytest.fixture(autouse=True, scope="class")
def schema():
    with mock.patch('json.load') as mock_json:
        mock_json.return_value = {
            "stack": {
                "type": "object", "properties": {
                    "name": "string"
                }
            }
        }
        with mock.patch('builtins.open', mock.mock_open(read_data=mock_json)):
            return Schema("path/schema.json")


@pytest.fixture()
def connection_manger():
    class ExampleConnectionManager(ConnectionManager):
        def call(self):
            pass

    cm = ExampleConnectionManager({"region": "eu-west-2"})
    return cm


@pytest.fixture(scope="module")
def provider():
    class ProviderA(Provider, registry_key='A'):
        pass

    return ProviderA


class TestProvider(object):
    def test_provider_instantiates_with_provider_name(
            self, schema, connection_manger
    ):
        provider = Provider('A', schema, connection_manger)
        assert provider.name == 'A'

    def test_provider_raises_value_error_if_provider_name_is_none(
            self, schema, provider
    ):
        connection_manager = {}
        with pytest.raises(ValueError):
            provider(None, schema, connection_manager)

    def test_provider_instantiates_with_correct_schema_type(
            self, schema, connection_manger, provider
    ):

        provider = Provider('C', schema, connection_manger)
        assert isinstance(provider.schema, ProviderSchema)

    def test_provider_instantiates_with_correct_connection_manager_type(
            self, schema, connection_manger
    ):
        provider = Provider('D', schema, connection_manger)
        assert isinstance(provider.connection_manager, ConnectionManager)

    def test_provider_raises_type_error_with_incorrect_connection_manager_property_type(
            self, schema
    ):
        connection_manager = {}
        with pytest.raises(TypeError):
            Provider('E', schema, connection_manager)

    def test_provider_raises_type_error_incorrect_schema_property_type(self, connection_manger):
        schema = {}
        with pytest.raises(TypeError):
            Provider('F', schema, connection_manger)


class TestProviderRegistry(object):
    def test_registry_automatically_registers_subclass(self, schema,
                                                       connection_manger,
                                                       provider):
        assert ProviderRegistry.registry()["A"] == provider
