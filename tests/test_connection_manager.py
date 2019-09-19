import pytest

from sceptre.providers.connection_manager import ConnectionManager


class TestConnectionManager(object):

    def test_connection_manager_instantiates_with_config(self):
        connection_config = {"profile": "prod", "region": "eu-west-1"}
        connection_manager = ConnectionManager(connection_config)
        assert connection_manager.config == connection_config

    def test_connection_manager_raises_type_error_with_invalid_config(self):
        connection_config = ("region", "eu-west-1")

        class ExampleConnectionManager(ConnectionManager):
            def __init__(self, config):
                super().__init__(config)

            def call(self):
                pass

        with pytest.raises(TypeError):
            ExampleConnectionManager(connection_config)

    def test_connection_manager_raises_value_error_with_empty_config(self):
        connection_config = {}

        class ExampleConnectionManager(ConnectionManager):
            def __init__(self, config):
                super().__init__(config)

            def call(self):
                pass

        with pytest.raises(ValueError):
            ExampleConnectionManager(connection_config)
