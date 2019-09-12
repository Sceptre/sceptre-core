# -*- coding: utf-8 -*-

"""
sceptre.providers.connection_manager

This module implements a ConnectionManager class, which simplifies and manages
Provider calls.
"""

import abc
import six
import logging
import threading


def _retry_provider_call(func):
    """
    Retries a Provider call up to 30 times if request rate limits are hit.

    The time waited between retries increases linearly. If rate limits are
    hit 30 times, _retry_provider_call raises a
    sceptre.exceptions.RetryLimitExceededException.

    :param func: A function that uses provider calls
    :type func: function
    :returns: The decorated function.
    :rtype: function
    :raises: sceptre.exceptions.RetryLimitExceededException
    """
    pass  # pragma: no cover


@six.add_metaclass(abc.ABCMeta)
class ConnectionManager(object):
    """
    The Connection Manager is used to create Provider clients for
    the various Provider services that Sceptre needs to interact with.

    :param profile: The Provider credentials profile that should be used.
    :type profile: str
    :param stack_name: The stack name for this connection.
    :type stack_name: str
    :param region: The region to use.
    :type region: str
    """

    _session_lock = threading.Lock()
    _client_lock = threading.Lock()
    _sessions = {}
    _clients = {}
    _stack_keys = {}

    def __init__(self, region, profile=None, stack_name=None):
        self.logger = logging.getLogger(__name__)

        self.region = region
        self.profile = profile
        self.stack_name = stack_name

        if stack_name:
            self._stack_keys[stack_name] = (region, profile)

    def __repr__(self):
        pass  # pragma: no cover

    def _get_session(self, profile, region=None):
        """
        Returns a Provider session in the target account.

        If a ``profile`` is specified in ConnectionManager's initialiser,
        then the profile is used to generate temporary credentials to create
        the Provider session. If ``profile`` is not specified then the default
        profile is assumed to create the Provider session.
        """
        pass  # pragma: no cover

    def _get_client(self, service, region, profile, stack_name):
        """
        Returns the client associated with <service>.
        """
        pass  # pragma: no cover

    @_retry_provider_call
    def call(
        self, service, command, kwargs=None, profile=None, region=None,
        stack_name=None
    ):
        """
        Makes a thread-safe Provider client call.
        """
        pass  # pragma: no cover
