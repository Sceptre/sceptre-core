# -*- coding: utf-8 -*-

"""
sceptre.provider.stack

This module implements a Stack class, which stores a Stack's data.

"""

import logging
from abc import ABC, abstractmethod
from typing import Mapping, Sequence


from sceptre.hooks import HookProperty
from sceptre.resolvers import ResolvableProperty


class Stack(ABC):
    """
    Stack stores information about a particular Provider Stack.
    """
    parameters = ResolvableProperty("parameters")
    _sceptre_user_data = ResolvableProperty("_sceptre_user_data")
    notifications = ResolvableProperty("notifications")
    hooks = HookProperty("hooks")

    def __init__(self, config):
        self.logger = logging.getLogger(__name__)
        if not isinstance(config, StackConfigData):
            raise TypeError("Config must be of type StackConfigData")
        self.config = config

    @abstractmethod
    def __repr__(self):
        """
        implementes the obj repr for a stack.
        """

    def __str__(self):
        """
        Returns the name of a stack.
        """
        return self.config.name

    @abstractmethod
    def __eq__(self, stack):
        """
        Should implement an equality check for stack data
        """

    def __hash__(self):
        """
        Implements a hash for stack for equality check
        """
        return hash(str(self))

    @property
    def sceptre_user_data(self):
        """Returns sceptre_user_data after ensuring that it is fully resolved.
         :rtype: dict or list or None
        """
        if not self._sceptre_user_data_is_resolved:
            self._sceptre_user_data_is_resolved = True
            self._resolve_sceptre_user_data()
        return self._sceptre_user_data

    @property
    @abstractmethod
    def template(self):
        """
        Returns the Provider Template used to create the Stack.

        :returns: The Stack's template.
        :rtype: SceptreTemplate
        """

    def _resolve_sceptre_user_data(self):
        data = self._sceptre_user_data
        if isinstance(data, Mapping):
            iterator = data.values()
        elif isinstance(data, Sequence):
            iterator = data
        else:
            return
        for value in iterator:
            if isinstance(value, ResolvableProperty.ResolveLater):
                value()


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
