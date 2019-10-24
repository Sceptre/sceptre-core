import json
import jsonschema

from abc import ABC, abstractmethod
from os import path

from sceptre.exceptions import InvalidProviderSchemaError


class ProviderSchema(ABC):

    @property
    @abstractmethod
    def path(self):
        """
        Is the path to the schema file
        """

    @property
    @abstractmethod
    def schema(self):
        """
        Is the loaded schema file in json schema format.
        """

    @abstractmethod
    def validate(self):
        """
        Validates a loaded schema.
        """


class Schema(ProviderSchema):
    VALID_SCHEMA_EXTENSION = '.json'

    def __init__(self, schema_path):
        self.path = schema_path
        self.schema = schema_path

    def validate(self, schema_type, instance):
        try:
            jsonschema.validate(
                instance=instance,
                schema=self.schema[schema_type]

            )
        except KeyError:
            raise KeyError("There was no schema for schema_type {}".format(schema_type))
        except jsonschema.ValidationError:
            raise jsonschema.ValidationError(
                "The {} config provided is invalid for schema {}".format(
                    schema_type, self.schema[schema_type]
                )
            )
        return True

    @property
    def path(self):
        return self.__path

    @path.setter
    def path(self, schema_path):
        filepath, ext = path.splitext(schema_path)
        if ext != self.VALID_SCHEMA_EXTENSION:
            raise InvalidProviderSchemaError(
                "ProviderSchema is the wrong file type, it must be {}".format(
                    self.VALID_SCHEMA_EXTENSION)
            )
        self.__path = schema_path

    @property
    def schema(self):
        return self.__schema

    @schema.setter
    def schema(self, schema_path):
        try:
            with open(schema_path) as schema:
                s = schema.read()
        except FileNotFoundError:
            raise FileNotFoundError(
                "ProviderSchema file {} not found".format(schema_path)
            )
        loaded_schema = json.load(s)
        if self._is_schema_valid(loaded_schema):
            self.__schema = loaded_schema

    def _is_schema_valid(self, schema):
        if "stack" in schema.keys():
            return True
        raise InvalidProviderSchemaError("The ProviderSchema does not contain valid keys")
