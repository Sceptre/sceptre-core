import pytest
import mock

from sceptre.providers.schema import ProviderSchema, Schema
from sceptre.providers import Provider
from sceptre.providers.connection_manager import ConnectionManager


class TestProvider(object):

    @mock.patch('json.load')
    @mock.patch('builtins.open')
    def test_provider_instantiates_with_correct_property_types(
            self, mock_open, mock_json
    ):
        mock_json.return_value = {
            "stack": {
                "type": "object", "properties": {
                        "name": "string"
                }
            }
        }
        schema = Schema("path/schema.json")

        class ExampleConnectionManager(ConnectionManager):
            def __init__(self, config):
                super().__init__(config)

            def call(self):
                pass
        connection_manager = ExampleConnectionManager({"region": "eu-west-2"})

        provider = Provider(schema, connection_manager)
        assert isinstance(provider.schema, ProviderSchema)
        assert isinstance(provider.connection_manager, ConnectionManager)

    @mock.patch('json.load')
    @mock.patch('builtins.open')
    def test_provider_raises_type_error_with_incorrect_connection_manager_property_type(
            self, mock_open, mock_json
    ):
        mock_json.return_value = {
            "stack": {
                "type": "object",
                "properties": {
                        "name": "string"
                }
            }
        }
        schema = Schema("path/schema.json")

        connection_manager = {}

        with pytest.raises(TypeError):
            provider = Provider(schema, connection_manager)
            assert isinstance(provider.schema, ProviderSchema)
            assert provider.schema == schema

    def test_provider_raises_type_error_with_incorrect_schema_property_type(self):
        schema = {}

        class ExampleConnectionManager(ConnectionManager):
            def __init__(self, config):
                super().__init__(config)

            def call(self):
                pass

        connection_manager = ExampleConnectionManager({"region": "eu-west-2"})

        with pytest.raises(TypeError):
            provider = Provider(schema, connection_manager)
            assert isinstance(provider.connection_manager, ConnectionManager)
            assert provider.connection_manager == connection_manager
