import jsonschema

from abc import ABC, abstractmethod

from sceptre.exceptions import InvalidProviderSchemaError


class SchemaInterface(ABC):

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


class Schema(SchemaInterface):

    def __init__(self, schema):
        self.schema = schema

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
    def schema(self):
        return self.__schema

    @schema.setter
    def schema(self, schema):
        if self._is_schema_valid(schema):
            self.__schema = schema

    def _is_schema_valid(self, schema):
        if "stack" in schema.keys():
            return True
        raise InvalidProviderSchemaError("The ProviderSchema does not contain valid keys")
