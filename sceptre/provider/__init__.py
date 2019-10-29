import re

from abc import ABC, abstractmethod

from sceptre.exceptions import DuplicateProviderRegistrationError
from sceptre.exceptions import ProviderNotFoundError

from sceptre.provider.schema import ProviderSchema
from sceptre.provider.connection_manager import ConnectionManager


class ProviderRegistry:
    __registry = {}

    @classmethod
    def register(cls, provider, provider_key):
        if provider_key in cls.__registry:
            raise DuplicateProviderRegistrationError("Provider {} already exists. You cannot have\
                                                     duplicate providers in the ProviderRegistry."
                                                     .format(provider_key))
        cls.__registry[provider_key] = provider

    @classmethod
    def registry(cls):
        return cls.__registry.copy()

    @classmethod
    def remove_provider(cls, key):
        cls.__registry.pop(key)

    @classmethod
    def get_provider(cls, name):
        try:
            return cls.__registry[name]
        except KeyError:
            raise ProviderNotFoundError(
                "Provider: {} is not found in the ProviderRegistry.".format(name))


class SceptreProvider(ABC):

    @property
    @abstractmethod
    def name(self):
        """
        Returns the name of the Provider
        """

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


class Provider(SceptreProvider):
    command_registry = {}

    def __init_subclass__(cls, registry_key, **kwargs):
        ProviderRegistry.register(cls, registry_key)
        super().__init_subclass__(**kwargs)

    def __init__(self, name, schema, connection_manager):
        self.name = name
        self.schema = schema
        self.connection_manager = connection_manager

    @property
    def name(self):
        return self.__name

    @name.setter
    def name(self, name):
        if name is None:
            raise ValueError('A provider name must not be none')
        self.__name = name

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


class Command:
    @abstractmethod
    def execute(self):
        """
        Implements the logic for the command
        """

    @classmethod
    def __init_subclass__(cls, provider=None, **kwargs):
        command_type = cls.__to_camel_case(cls.__name__).split('_')[0]
        command_name = cls.__to_camel_case(cls.__name__)
        if not isinstance(provider, SceptreProvider):
            raise TypeError("The provider {} supplied to the Command {} \
                            is not of Type sceptre.provider.Provider".format(provider,
                                                                             command_name)
                            )
        provider.command_registry.update({command_type: {command_name: cls}})
        super().__init_subclass__(**kwargs)

    def __to_camel_case(name):
        s1 = re.sub('(.)([A-Z][a-z]+)', r'\1_\2', name)
        return re.sub('([a-z0-9])([A-Z])', r'\1_\2', s1).lower()
