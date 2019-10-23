import pytest
from unittest import mock

from jsonschema import ValidationError

from sceptre.providers.schema import Schema
from sceptre.exceptions import InvalidProviderSchemaError


class TestSchema:
    def setup_method(self, test_method):
        pass

    @mock.patch('json.load')
    @mock.patch('builtins.open')
    def test_schema_instantiates_with_path(self, mock_open, mock_json):
        schema_path = "provider/schema_path.json"
        mock_json.return_value = {'stack': 'hello'}
        schema = Schema(schema_path)
        mock_open.assert_called_once_with("provider/schema_path.json")
        assert schema.path == schema_path

    @mock.patch('json.load')
    @mock.patch('builtins.open')
    def test_invalid_schema_file_raises_error(self, mock_open, mock_json):
        mock_json.return_value = {"stack": "value1"}
        schema_path = "incorrect/schema.py"
        with pytest.raises(InvalidProviderSchemaError):
            Schema(schema_path)

    @mock.patch('builtins.open')
    def test_schema_file_not_found(self, mock_open):
        mock_open.side_effect = FileNotFoundError
        with pytest.raises(FileNotFoundError):
            schema = Schema("test_schema_file_not_foundno_path/schema.json")
            assert schema.path is None

    @mock.patch('json.load')
    @mock.patch('builtins.open')
    def test_correct_schema_validates_successfully(self, mock_open, mock_json):
        schema_path = "provider/schema_path.json"
        mock_json.return_value = {"stack": "value1"}
        schema = Schema(schema_path)
        s = {"stack": "value1"}
        assert schema.schema == s
        assert schema._is_schema_valid(s) is True

    @mock.patch('json.load')
    @mock.patch('builtins.open')
    def test_valid_schema_file_fails_validation(self, mock_open, mock_json):
        schema_path = "provider/schema_path.json"
        mock_json.return_value = {"stack": "value1"}
        schema = Schema(schema_path)
        s = {"blah": "value1"}
        with pytest.raises(InvalidProviderSchemaError):
            schema._is_schema_valid(s)

    @mock.patch('json.loads')
    @mock.patch('builtins.open')
    def test_validate_schema_with_valid_schmea(self, mock_open, mock_json):
        schema_definition = {
            "stack": {
                "type": "object",
                "properties": {
                    "name": {"type": "string"}
                }
            }
        }

        schema_path = "provider/schema_path.json"
        mock_json.return_value = schema_definition
        schema = Schema(schema_path)
        assert schema.schema == schema_definition
        assert schema.validate("stack", {"name": "hello"}) is True

    @mock.patch('json.loads')
    @mock.patch('builtins.open')
    def test_validate_schema_with_invalid_schmea_type_raises_key_error(self, mock_open, mock_json):
        schema_definition = {
            "stack": {
                "type": "object",
                "properties": {
                    "name": {"type": "string"}
                }
            }
        }
        schema_path = "provider/schema_path.json"
        mock_json.return_value = schema_definition
        schema = Schema(schema_path)
        assert schema.schema == schema_definition
        with pytest.raises(KeyError):
            schema.validate("blah", {"name": "hello"})

    @mock.patch('json.loads')
    @mock.patch('builtins.open')
    def test_validate_schema_with_invalid_schmea_raises_validation_error(
            self, mock_open, mock_json
    ):
        schema_definition = {
            "stack": {
                "type": "object",
                "properties": {
                    "name": {"type": "string"}
                },
                "required": ["name"]
            }
        }
        schema_path = "provider/schema_path.json"
        mock_json.return_value = schema_definition
        schema = Schema(schema_path)
        assert schema.schema == schema_definition
        with pytest.raises(ValidationError):
            schema.validate("stack", {"region": "westA"})
