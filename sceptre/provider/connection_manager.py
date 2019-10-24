# -*- coding: utf-8 -*-

"""
sceptre.provider.connection_manager

This module implements a ConnectionManager class, which simplifies and manages
Provider calls.
"""

import functools
import logging

from abc import ABC, abstractmethod

from sceptre.exceptions import ClientError, RetryLimitExceededError


class ConnectionManager(ABC):
    """
    The Connection Manager defines what Provider ConnectionManagers should implement
    clients for the various Provider services that Sceptre needs to interact with.

    :param config: The attributes required to configure a ConnectionManager
    :type config: dict
    """

    def __init__(self, config):
        self.logger = logging.getLogger(__name__)
        self.config = config

    def _retry_provider_call(self, func):
        """
        Retries a Provider call if request rate limits are hit.

        The time waited between retries increases linearly. If rate limits are
        hit 30 times, _retry_provider_call raises a
        sceptre.exceptions.RetryLimitExceededException.

        :param func: A function that uses provider calls
        :type func: function
        :returns: The decorated function.
        :rtype: function
        :raises: sceptre.exceptions.RetryLimitExceededException
        """

        @functools.wraps(func)
        def decorated(*args, **kwargs):
            max_retries = 29
            attempts = 0
            while attempts < max_retries:
                try:
                    return func(*args, **kwargs)
                except ClientError as e:
                    attempts += 1
            raise RetryLimitExceededError(
                "Exceeded request limit {} times. Aborting.".format(max_retries)
            )
        return decorated

    @property
    @abstractmethod
    def call(self):
        """
        Makes a thread-safe Provider client call.
        """

    @property
    def config(self):
        return self.__config

    @config.setter
    def config(self, config):
        if not isinstance(config, dict):
            raise TypeError("ConnectionManager config must be of type dict")
        elif any(config) is False:
            raise ValueError("ConnectionManager config cannot be empty")
        else:
            self.__config = config
