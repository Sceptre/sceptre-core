# -*- coding: utf-8 -*-

"""
sceptre.providers.aws.connection_manager

This module implements a ConnectionManager class, which simplifies and manages
Boto3 calls.
"""

import abc
import six
import logging
import threading


def _retry_boto_call(func):
    """
    Retries a Boto3 call up to 30 times if request rate limits are hit.

    The time waited between retries increases linearly. If rate limits are
    hit 30 times, _retry_boto_call raises a
    sceptre.exceptions.RetryLimitExceededException.

    :param func: A function that uses boto calls
    :type func: function
    :returns: The decorated function.
    :rtype: function
    :raises: sceptre.exceptions.RetryLimitExceededException
    """
    pass  # pragma: no cover


@six.add_metaclass(abc.ABCMeta)
class ConnectionManager(object):
    """
    The Connection Manager is used to create boto3 clients for
    the various AWS services that Sceptre needs to interact with.

    :param profile: The AWS credentials profile that should be used.
    :type profile: str
    :param stack_name: The CloudFormation stack name for this connection.
    :type stack_name: str
    :param region: The region to use.
    :type region: str
    """

    _session_lock = threading.Lock()
    _client_lock = threading.Lock()
    _boto_sessions = {}
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
        Returns a boto session in the target account.

        If a ``profile`` is specified in ConnectionManager's initialiser,
        then the profile is used to generate temporary credentials to create
        the Boto session. If ``profile`` is not specified then the default
        profile is assumed to create the boto session.

        :returns: The Boto3 session.
        :rtype: boto3.session.Session
        :raises: botocore.exceptions.ClientError
        """
        pass  # pragma: no cover

    def _get_client(self, service, region, profile, stack_name):
        """
        Returns the Boto3 client associated with <service>.

        Equivalent to calling Boto3.client(<service>). Gets the client using
        ``boto_session``.

        :param service: The Boto3 service to return a client for.
        :type service: str
        :returns: The Boto3 client.
        :rtype: boto3.client.Client
        """
        pass  # pragma: no cover

    @_retry_boto_call
    def call(
        self, service, command, kwargs=None, profile=None, region=None,
        stack_name=None
    ):
        """
        Makes a thread-safe Boto3 client call.

        Equivalent to ``boto3.client(<service>).<command>(**kwargs)``.

        :param service: The Boto3 service to return a client for.
        :type service: str
        :param command: The Boto3 command to call.
        :type command: str
        :param kwargs: The keyword arguments to supply to <command>.
        :type kwargs: dict
        :returns: The response from the Boto3 call.
        :rtype: dict
        """
        pass  # pragma: no cover
