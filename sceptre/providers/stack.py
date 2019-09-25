# -*- coding: utf-8 -*-

"""
sceptre.providers.stack

This module implements a Stack class, which stores a Stack's data.

"""

import logging
from abc import ABC, abstractmethod
from typing import Mapping, Sequence


from sceptre.hooks import HookProperty
from sceptre.hooks import add_stack_hooks
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

    @abstractmethod
    def get_external_stack_name(self):
        """
        Implements the external name for the stack
        """

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

    @add_stack_hooks
    @abstractmethod
    def create(self):
        """
        Creates a Stack.

        :returns: The Stack's status.
        :rtype: sceptre.providers.stack_status.StackStatus
        """

    @add_stack_hooks
    @abstractmethod
    def update(self):
        """
        Updates the Stack.

        :returns: The Stack's status.
        :rtype: sceptre.providers.stack_status.StackStatus
        """

    @add_stack_hooks
    @abstractmethod
    def delete(self):
        """
        Deletes the Stack.

        :returns: The Stack's status.
        :rtype: sceptre.providers.stack_status.StackStatus
        """

    @abstractmethod
    def launch(self):
        """
        Launches the Stack.

        If the Stack status is create_failed or rollback_complete, the
        Stack is deleted. Launch then tries to create or update the Stack,
        depending if it already exists. If there are no updates to be
        performed, launch exits gracefully.

        :returns: The Stack's status.
        :rtype: sceptre.providers.stack_status.StackStatus
        """

    @abstractmethod
    def cancel_stack_update(self):
        """
        Cancels a Stack update.

        :returns: The cancelled Stack status.
        :rtype: sceptre.providers.stack_status.StackStatus
        """

    @abstractmethod
    def lock(self):
        """
        Locks the Stack by applying a deny-all updates Stack Policy.
        """

    @abstractmethod
    def unlock(self):
        """
        Unlocks the Stack by applying an allow-all updates Stack Policy.
        """

    @abstractmethod
    def describe(self):
        """
        Returns the a description of the Stack.

        :returns: A Stack description.
        :rtype: dict
        """

    @abstractmethod
    def describe_events(self):
        """
        Returns the Provider events for a Stack.

        :returns: Provider events for a Stack.
        :rtype: dict
        """

    @abstractmethod
    def describe_resources(self):
        """
        Returns the logical and physical resource IDs of the Stack's resources.

        :returns: Information about the Stack's resources.
        :rtype: dict
        """

    @abstractmethod
    def describe_outputs(self):
        """
        Returns the Stack's outputs.

        :returns: The Stack's outputs.
        :rtype: list
        """

    @abstractmethod
    def continue_update_rollback(self):
        """
        Rolls back a Stack in the UPDATE_ROLLBACK_FAILED state to
        UPDATE_ROLLBACK_COMPLETE.
        """

    @abstractmethod
    def set_policy(self):
        """
        Applies a Stack Policy.

        :param policy_path: The relative path of JSON file containing\
                the Provider Policy to apply.
        :type policy_path: str
        """

    @abstractmethod
    def get_policy(self):
        """
        Returns a Stack's Policy.

        :returns: The Stack's Stack Policy.
        :rtype: str
        """

    @abstractmethod
    def create_change_set(self):
        """
        Creates a Change Set with the name ``change_set_name``.

        :param change_set_name: The name of the Change Set.
        :type change_set_name: str
        """

    @abstractmethod
    def delete_change_set(self):
        """
        Deletes the Change Set ``change_set_name``.

        :param change_set_name: The name of the Change Set.
        :type change_set_name: str
        """

    @abstractmethod
    def describe_change_set(self):
        """
        Describes the Change Set ``change_set_name``.

        :param change_set_name: The name of the Change Set.
        :type change_set_name: str
        :returns: The description of the Change Set.
        :rtype: dict
        """

    @abstractmethod
    def execute_change_set(self):
        """
        Executes the Change Set ``change_set_name``.

        :param change_set_name: The name of the Change Set.
        :type change_set_name: str
        :returns: The Stack status
        :rtype: str
        """

    @abstractmethod
    def list_change_sets(self):
        """
        Lists the Stack's Change Sets.

        :returns: The Stack's Change Sets.
        :rtype: dict or list
        """

    @abstractmethod
    def generate(self):
        """
        Returns the Template for the Stack
        """

    @abstractmethod
    def validate(self):
        """
        Validates the Stack's Provider Template.

        Raises an error if the Template is invalid.

        :returns: Validation information about the Template.
        :rtype: dict
        :raises: sceptre.exceptions.ClientError
        """

    @abstractmethod
    def estimate_cost(self):
        """
        Estimates a Stack's cost.

        :returns: An estimate of the Stack's cost.
        :rtype: dict
        :raises: sceptre.exceptions.ClientError
        """

    @abstractmethod
    def get_status(self):
        """
        Returns the Stack's status.

        :returns: The Stack's status.
        :rtype: sceptre.providers.stack_status.StackStatus
        """


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
