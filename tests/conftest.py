import pytest

from sceptre.provider.schema import Schema
from sceptre.provider.connection_manager import ConnectionManager
from sceptre.provider import Provider
from sceptre.provider import ProviderRegistry
from sceptre.provider.stack import StackConfigData


@pytest.fixture(autouse=True, scope="session")
def schema():
    schema_definition = {
        "stack": {
            "type": "object", "properties": {
                "name": "string"
            }
        }
    }
    return Schema(schema_definition)


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
