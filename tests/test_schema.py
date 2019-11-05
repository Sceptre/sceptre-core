import pytest

from jsonschema import ValidationError

from sceptre.provider.schema import Schema


class TestSchema:

    def test_correct_schema_validates_successfully(self):
        schema_definition = {"stack": "value1"}
        schema = Schema(schema_definition)
        assert schema.schema == schema_definition
        assert schema._is_schema_valid(schema_definition) is True

    def test_validate_schema_with_valid_schmea(self):
        schema_definition = {
            "stack": {
                "type": "object",
                "properties": {
                    "name": {"type": "string"}
                }
            }
        }

        schema = Schema(schema_definition)
        assert schema.schema == schema_definition
        assert schema.validate("stack", {"name": "hello"}) is True

    def test_validate_schema_with_invalid_schmea_type_raises_key_error(self):
        schema_definition = {
            "stack": {
                "type": "object",
                "properties": {
                    "name": {"type": "string"}
                }
            }
        }
        schema = Schema(schema_definition)
        assert schema.schema == schema_definition
        with pytest.raises(KeyError):
            schema.validate("blah", {"name": "hello"})

    def test_validate_schema_with_invalid_schmea_raises_validation_error(self):
        schema_definition = {
            "stack": {
                "type": "object",
                "properties": {
                    "name": {"type": "string"}
                },
                "required": ["name"]
            }
        }
        schema = Schema(schema_definition)
        assert schema.schema == schema_definition
        with pytest.raises(ValidationError):
            schema.validate("stack", {"region": "westA"})
