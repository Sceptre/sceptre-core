from unittest import mock
import pytest

from sceptre.provider.schema import Schema
from sceptre.provider.connection_manager import ConnectionManager
from sceptre.provider import Provider
from sceptre.provider import ProviderRegistry
from sceptre.provider.stack import StackConfigData


@pytest.fixture(autouse=True, scope="session")
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


@pytest.fixture("module")
def connection_manager():
    class ExampleConnectionManager(ConnectionManager):
        def call(self):
            pass
    cm = ExampleConnectionManager({"region": "eu-west-2"})
    yield cm
    del cm


@pytest.fixture(scope="module")
def provider(schema, connection_manager):
    class ProviderA(Provider, registry_key='A'):
        pass

    yield ProviderA('A', schema, connection_manager)

    ProviderRegistry.remove_provider('A')
    del ProviderA


@pytest.fixture(scope='function')
def stack_config():
    return StackConfigData({"provider": "A",
                            "name": "Stack1",
                            "region": "eu-west-1",
                            'template_path': 'templates/vpc.json'
                            })
