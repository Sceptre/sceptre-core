# -*- coding: utf-8 -*-

"""
sceptre.provider.stack

This module implements a Stack class, which stores a Stack's data.
"""

import logging
import hashlib


class Stack:
    """
    Stack stores information about a particular Provider Stack.
    """

    def __init__(self, stack_id, config):
        self.logger = logging.getLogger(__name__)
        if not isinstance(config, StackConfigData):
            raise TypeError("Config must be of type StackConfigData")
        self.config = config
        self.id = self.__hash_id(stack_id)

    def __repr__(self):
        return(
            "sceptre.provider.stack.Stack("
            "id={stack_id}, "
            "config={config}"
            ")".format(
                stack_id=self.id,
                config=self.config
            )
        )

    def __str__(self):
        return self.config.name

    def __eq__(self, stack):
        return(
            self.id == stack.id and
            self.config == stack.config
        )

    def __hash__(self):
        return hash(str(self))

    def __hash_id(self, stack_id):
        return hashlib.sha256(stack_id.encode('utf-8')).hexdigest()


class StackConfigData(dict):
    def __getattr__(self, attr):
        if attr in self:
            return self[attr]
        else:
            raise AttributeError("No attribute {} on StackConfigData".format(attr))

    def __setattr__(self, attr, value):
        self[attr] = value

    def __delattr__(self, attr):
        if attr in self:
            del self[attr]
        else:
            raise AttributeError("No attribute {} on StackConfigData".format(attr))
