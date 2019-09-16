# -*- coding: utf-8 -*-

"""
sceptre.providers.actions

This module implements the StackActions class which provides the functionality
available to a Stack.
"""
import abc
import logging
import six

from sceptre.providers.connection_manager import ConnectionManager
from sceptre.hooks import add_stack_hooks


@six.add_metaclass(abc.ABCMeta)
class StackActions(object):
    """
    StackActions stores the operations a Stack can take, such as creating or
    deleting the Stack.

    :param stack: A Stack object
    :type stack: sceptre.providers.stack.Stack
    """

    __metaclass__ = abc.ABCMeta

    def __init__(self, stack):
        self.stack = stack
        self.name = self.stack.config.name
        self.logger = logging.getLogger(__name__)
        self.connection_manager = ConnectionManager(
            self.stack.config.region, self.stack.config.profile, self.stack.config.external_name
        )

    @add_stack_hooks
    def create(self):
        """
        Creates a Stack.

        :returns: The Stack's status.
        :rtype: sceptre.providers.stack_status.StackStatus
        """
        pass  # pragma: no cover

    @add_stack_hooks
    def update(self):
        """
        Updates the Stack.

        :returns: The Stack's status.
        :rtype: sceptre.providers.stack_status.StackStatus
        """
        pass  # pragma: no cover

    @add_stack_hooks
    def delete(self):
        """
        Deletes the Stack.

        :returns: The Stack's status.
        :rtype: sceptre.providers.stack_status.StackStatus
        """
        pass  # pragma: no cover

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
        pass  # pragma: no cover

    def cancel_stack_update(self):
        """
        Cancels a Stack update.

        :returns: The cancelled Stack status.
        :rtype: sceptre.providers.stack_status.StackStatus
        """
        pass  # pragma: no cover

    def lock(self):
        """
        Locks the Stack by applying a deny-all updates Stack Policy.
        """
        pass  # pragma: no cover

    def unlock(self):
        """
        Unlocks the Stack by applying an allow-all updates Stack Policy.
        """
        pass  # pragma: no cover

    def describe(self):
        """
        Returns the a description of the Stack.

        :returns: A Stack description.
        :rtype: dict
        """
        pass  # pragma: no cover

    def describe_events(self):
        """
        Returns the Provider events for a Stack.

        :returns: Provider events for a Stack.
        :rtype: dict
        """
        pass  # pragma: no cover

    def describe_resources(self):
        """
        Returns the logical and physical resource IDs of the Stack's resources.

        :returns: Information about the Stack's resources.
        :rtype: dict
        """
        pass  # pragma: no cover

    def describe_outputs(self):
        """
        Returns the Stack's outputs.

        :returns: The Stack's outputs.
        :rtype: list
        """
        pass  # pragma: no cover

    def continue_update_rollback(self):
        """
        Rolls back a Stack in the UPDATE_ROLLBACK_FAILED state to
        UPDATE_ROLLBACK_COMPLETE.
        """
        pass  # pragma: no cover

    def set_policy(self):
        """
        Applies a Stack Policy.

        :param policy_path: The relative path of JSON file containing\
                the Provider Policy to apply.
        :type policy_path: str
        """
        pass  # pragma: no cover

    def get_policy(self):
        """
        Returns a Stack's Policy.

        :returns: The Stack's Stack Policy.
        :rtype: str
        """
        pass  # pragma: no cover

    def create_change_set(self):
        """
        Creates a Change Set with the name ``change_set_name``.

        :param change_set_name: The name of the Change Set.
        :type change_set_name: str
        """
        pass  # pragma: no cover

    def delete_change_set(self):
        """
        Deletes the Change Set ``change_set_name``.

        :param change_set_name: The name of the Change Set.
        :type change_set_name: str
        """
        pass  # pragma: no cover

    def describe_change_set(self):
        """
        Describes the Change Set ``change_set_name``.

        :param change_set_name: The name of the Change Set.
        :type change_set_name: str
        :returns: The description of the Change Set.
        :rtype: dict
        """
        pass  # pragma: no cover

    def execute_change_set(self):
        """
        Executes the Change Set ``change_set_name``.

        :param change_set_name: The name of the Change Set.
        :type change_set_name: str
        :returns: The Stack status
        :rtype: str
        """
        pass  # pragma: no cover

    def list_change_sets(self):
        """
        Lists the Stack's Change Sets.

        :returns: The Stack's Change Sets.
        :rtype: dict or list
        """
        pass  # pragma: no cover

    def generate(self):
        """
        Returns the Template for the Stack
        """
        pass  # pragma: no cover

    def validate(self):
        """
        Validates the Stack's Provider Template.

        Raises an error if the Template is invalid.

        :returns: Validation information about the Template.
        :rtype: dict
        :raises: sceptre.exceptions.ClientError
        """
        pass  # pragma: no cover

    def estimate_cost(self):
        """
        Estimates a Stack's cost.

        :returns: An estimate of the Stack's cost.
        :rtype: dict
        :raises: sceptre.exceptions.ClientError
        """
        pass  # pragma: no cover

    def get_status(self):
        """
        Returns the Stack's status.

        :returns: The Stack's status.
        :rtype: sceptre.providers.stack_status.StackStatus
        """
        pass  # pragma: no cover
