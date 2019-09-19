from abc import ABC, abstractmethod

from sceptre.providers.schema import ProviderSchema
from sceptre.providers.connection_manager import ConnectionManager


class ProviderInterface(ABC):

    @property
    @abstractmethod
    def connection_manager(self):
        """
        Returns the ConnectionManager for a given Provider.
        """

    @property
    @abstractmethod
    def schema(self):
        """
        Returns the ProviderSchema for a given Provider.
        """


class Provider(ProviderInterface):
    def __init__(self, schema, connection_manager):
        self.schema = schema
        self.connection_manager = connection_manager

    @property
    def schema(self):
        return self.__schema

    @schema.setter
    def schema(self, schema):
        if not isinstance(schema, ProviderSchema):
            raise TypeError(
                "The schema provided is not of type ProviderSchema,\
                        it is type {}.".format(type(schema)))
        else:
            self.__schema = schema

    @property
    def connection_manager(self):
        return self.__connection_manager

    @connection_manager.setter
    def connection_manager(self, connection_manager):
        if not isinstance(connection_manager, ConnectionManager):
            raise TypeError("The ConnectionManager provided is not of correct\
                            type ConnectionManager, it is type {}.".format(
                type(connection_manager))
            )
        else:
            self.__connection_manager = connection_manager
