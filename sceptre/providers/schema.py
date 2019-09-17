import json
from os import path
from sceptre.exceptions import InvalidProviderSchemaError


class ProviderSchema(object):
    VALID_SCHEMA_EXTENSION = '.json'

    def __init__(self, schema_path):
        self.path = schema_path
        self._schema_file_type_is_valid(self.path)
        try:
            with open(self.path) as schema:
                s = schema.read()
        except FileNotFoundError:
            raise FileNotFoundError("ProviderSchema file {} not found".format(self.path))
        else:
            loaded_schema = json.load(s)
            if self._is_schema_valid(loaded_schema):
                self.schema = loaded_schema

    def _schema_file_type_is_valid(self, schema_path):
        filepath, ext = path.splitext(schema_path)
        if ext != self.VALID_SCHEMA_EXTENSION:
            raise InvalidProviderSchemaError(
                "ProviderSchema is the wrong file type, it must be {}".format(
                    self.VALID_SCHEMA_EXTENSION)
            )

    def _is_schema_valid(self, schema):
        if "stack" in schema.keys():
            return True
        else:
            raise InvalidProviderSchemaError("The ProviderSchema does not contain valid keys")
