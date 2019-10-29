# -*- coding: utf-8 -*-

"""
sceptre.provider.stack

This module implements a Stack class, which stores a Stack's data.
"""

import logging

from sceptre.provider import ProviderRegistry


class Stack:
    """
    Stack stores information about a particular Provider Stack.
    """

    def __init__(self, stack_id, config):
        self.logger = logging.getLogger(__name__)
        if not isinstance(config, StackConfigData):
            raise TypeError("Config must be of type StackConfigData")
        self.config = config
        self.id = stack_id
        self.provider = ProviderRegistry.get_provider(config.provider)

    def __repr__(self):
        return(
            "sceptre.provider.stack.Stack("
            "id={stack_id}, "
            "config={config}, "
            "provider={provider}"
            ")".format(
                stack_id=self.id,
                config=self.config,
                provider=self.provider
            )
        )

    def __str__(self):
        return self.id

    def __eq__(self, stack):
        return(
            self.id == stack.id
        )

    def __hash__(self):
        return hash(str(self))


class StackConfigData(dict):
    def __getattr__(self, attr):
        if attr in self:
            return self[attr]
        return None

    def __setattr__(self, attr, value):
        self[attr] = value

    def __delattr__(self, attr):
        if attr in self:
            del self[attr]
        else:
            raise AttributeError("No attribute {} on StackConfigData".format(attr))
