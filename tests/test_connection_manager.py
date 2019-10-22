import pytest
from unittest import mock

from sceptre.providers.connection_manager import ConnectionManager
from sceptre.exceptions import ClientError
from sceptre.exceptions import RetryLimitExceededError


class TestConnectionManager(object):

    def test_connection_manager_instantiates_with_config(self):
        connection_config = {"profile": "prod", "region": "eu-west-1"}

        class ExampleConnectionManager(ConnectionManager):
            def call(self):
                pass

        connection_manager = ExampleConnectionManager(connection_config)
        assert connection_manager.config == connection_config

    def test_connection_manager_raises_type_error_with_invalid_config(self):
        connection_config = ("region", "eu-west-1")

        class ExampleConnectionManager(ConnectionManager):
            def call(self):
                pass

        with pytest.raises(TypeError):
            ExampleConnectionManager(connection_config)

    def test_connection_manager_raises_value_error_with_empty_config(self):
        connection_config = {}

        class ExampleConnectionManager(ConnectionManager):
            def call(self):
                pass

        with pytest.raises(ValueError):
            ExampleConnectionManager(connection_config)

    def test_retry_provider_call_retries_max_attemps(self):
        MAX_RETRY_COUNT = 29
        connection_config = {"region": "eu-west-1"}
        mock_fn = mock.Mock()
        mock_fn.side_effect = ClientError

        class ExampleConnectionManager(ConnectionManager):
            def call(self):
                pass

        with pytest.raises(RetryLimitExceededError):
            connection_manager = ExampleConnectionManager(connection_config)
            connection_manager._retry_provider_call(mock_fn)()

        assert MAX_RETRY_COUNT == mock_fn.call_count
