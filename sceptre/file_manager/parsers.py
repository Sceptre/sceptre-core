import logging

from pkg_resources import iter_entry_points

import yaml

from sceptre.exceptions import SceptreYamlError


class SceptreYamlParser:
    def __init__(self):
        self.logger = logging.getLogger(__name__)
        self.__add_yaml_constructors(["sceptre.hooks", "sceptre.resolver"])

    def load(self, stream):
        try:
            data = yaml.load(stream, Loader=yaml.FullLoader)
        except yaml.YAMLError:
            raise SceptreYamlError(
                "The stream {} could not be parsed.".format(stream))
        return data

    def __add_yaml_constructors(self, entry_point_groups):
        """
        Adds PyYAML constructor functions for all classes found registered at
        the given entry point groups. Classes are registered whereby the node
        tag is the entry point name.
        :param entry_point_groups: Names of entry point groups.
        :type entry_point_groups: list
        """
        self.logger.info(
            "Adding yaml constructors for the entry point groups {0}".format(
                entry_point_groups
            )
        )

        def constructor_factory(node_class):
            """
            Returns constructor that will initialise objects from a
            given node class.
            :param node_class: Class representing the node.
            :type node_class: class
            :returns: Class initialiser.
            :rtype: func
            """
            # This function signture is required by PyYAML
            def class_constructor(loader, node):
                return node_class(
                    loader.construct_scalar(node)
                )  # pragma: no cover

            return class_constructor

        for group in entry_point_groups:
            for entry_point in iter_entry_points(group):
                # Retrieve name and class from entry point
                node_tag = u'!' + entry_point.name
                node_class = entry_point.load()

                # Add constructor to PyYAML loader
                yaml.FullLoader.add_constructor(
                    node_tag, constructor_factory(node_class)
                )
                self.logger.debug(
                    "Added constructor for %s with node tag %s",
                    str(node_class), node_tag
                )
