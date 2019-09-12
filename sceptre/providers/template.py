# -*- coding: utf-8 -*-

"""
sceptre.providers.template

This module implements a Template class, which stores a Provider template
and implements methods for uploading it to S3.
"""

import abc
import logging
import os
import six


@six.add_metaclass(abc.ABCMeta)
class Template(object):
    """
    Template represents a IaC Template. It is responsible for
    loading, storing and optionally uploading local templates for use by the Provider.

    :param path: The absolute path to the file which stores the template.
    :type path: str

    :param sceptre_user_data: A dictionary of arbitrary data to be passed to\
            a handler function in an external Python script.
    :type sceptre_user_data: dict

    :param connection_manager:
    :type connection_manager: sceptre.providers.connection_manager.ConnectionManager

    :param template_details:
    :type template_details: dict
    """
    __metaclass__ = abc.ABCMeta

    def __init__(
        self, path, sceptre_user_data, connection_manager=None, template_details=None
    ):
        self.logger = logging.getLogger(__name__)

        self.path = path
        self.sceptre_user_data = sceptre_user_data
        self.connection_manager = connection_manager
        self.template = template_details

        self.name = os.path.basename(path).split(".")[0]
        self._body = None

    def __repr__(self):
        return (
            "sceptre.providers.template.Template(name='{0}', path='{1}', "
            "sceptre_user_data={2}, s3_details={3})".format(
                self.name, self.path, self.sceptre_user_data, self.s3_details
            )
        )

    @property
    def body(self):
        """
        Represents body of the template.

        :returns: The body of the template.
        :rtype: str
        """
        pass

    def _call_sceptre_handler(self):
        """
        Calls the function `sceptre_handler` within templates that are python
        scripts.

        :returns: The string returned from sceptre_handler in the template.
        :rtype: str
        :raises: IOError
        :raises: TemplateSceptreHandlerError
        """
        pass

    def upload_to_s3(self):
        """
        Uploads the template to ``bucket_name`` and returns its URL.

        The Template is uploaded with the ``bucket_key``.

        :returns: The URL of the Template object in S3.
        :rtype: str
        :raises: sceptre.exceptions.ClientError

        """
        pass

    def _bucket_exists(self):
        """
        Checks if the bucket ``bucket_name`` exists.

        :returns: Boolean whether the bucket exists
        :rtype: bool
        :raises: sceptre.exceptions.ClientError

        """
        pass

    def _create_bucket(self):
        """
        Create the s3 bucket ``bucket_name``.

        :raises: sceptre.exceptions.ClientError

        """
        pass

    def get_provider_call_parameter(self):
        """
        Returns the template location.

        Uploads the template and returns the object's URL, or returns
        the template itself.

        :returns: The call parameter for the template.
        :rtype: dict
        """
        pass

    @staticmethod
    def _render_jinja_template(template_dir, filename, jinja_vars):
        """
        Renders a jinja template.

        Sceptre supports passing sceptre_user_data to JSON and YAML
        templates using Jinja2 templating.

        :param template_dir: The directory containing the template.
        :type template_dir: str
        :param filename: The name of the template file.
        :type filename: str
        :param jinja_vars: Dict of variables to render into the template.
        :type jinja_vars: dict
        :returns: The body of the template.
        :rtype: str
        """
        pass
