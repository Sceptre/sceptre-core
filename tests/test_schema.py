import pytest
import mock

from sceptre.providers.schema import ProviderSchema
from sceptre.exceptions import InvalidProviderSchemaError


class TestSchema(object):
    def setup_method(self, test_method):
        pass

    @mock.patch('json.load')
    @mock.patch('builtins.open')
    def test_schema_instantiates_with_path(self, mock_open, mock_json):
        schema_path = "provider/schema_path.json"
        mock_json.return_value = {'stack': 'hello'}
        schema = ProviderSchema(schema_path)
        mock_open.assert_called_once_with("provider/schema_path.json")
        assert schema.path == schema_path

    @mock.patch('json.load')
    @mock.patch('builtins.open')
    def test_invalid_schema_file_raises_error(self, mock_open, mock_json):
        schema_path = "provider/schema_path.json"
        mock_json.return_value = {"stack": "value1"}
        schema = ProviderSchema(schema_path)
        invalid_schema_ext = "incorrect/schema.py"
        with pytest.raises(InvalidProviderSchemaError):
            schema._schema_file_type_is_valid(invalid_schema_ext)

    @mock.patch('builtins.open')
    def test_schema_file_not_found(self, mock_open):
        mock_open.side_effect = FileNotFoundError
        with pytest.raises(FileNotFoundError):
            schema = ProviderSchema("test_schema_file_not_foundno_path/schema.json")
            assert schema.path is None

    @mock.patch('json.load')
    @mock.patch('builtins.open')
    def test_correct_schema_validates_successfully(self, mock_open, mock_json):
        schema_path = "provider/schema_path.json"
        mock_json.return_value = {"stack": "value1"}
        schema = ProviderSchema(schema_path)
        s = {"stack": "value1"}
        assert schema.schema == s
        assert schema._is_schema_valid(s) is True

    @mock.patch('json.load')
    @mock.patch('builtins.open')
    def test_valid_schema_file_fails_validation(self, mock_open, mock_json):
        schema_path = "provider/schema_path.json"
        mock_json.return_value = {"stack": "value1"}
        schema = ProviderSchema(schema_path)
        s = {"blah": "value1"}
        with pytest.raises(InvalidProviderSchemaError):
            schema._is_schema_valid(s)
