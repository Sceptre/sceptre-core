import re

from abc import abstractmethod

from sceptre.providers import SceptreProvider


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
                            is not of Type sceptre.providers.Provider".format(provider,
                                                                              command_name)
                            )
        provider.command_registry.update({command_type: {command_name: cls}})
        super().__init_subclass__(**kwargs)

    def __to_camel_case(name):
        s1 = re.sub('(.)([A-Z][a-z]+)', r'\1_\2', name)
        return re.sub('([a-z0-9])([A-Z])', r'\1_\2', s1).lower()
