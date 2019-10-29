# -*- coding: utf-8 -*-

"""
sceptre.config.graph

This module implements a StackGraph, which is represented as a directed
acyclic graph of a Stack's dependencies.
"""

import logging
import re
import networkx as nx
from sceptre.exceptions import CircularDependenciesError


class StackGraph:
    """
    A Directed Acyclic Graph representing the relationship between a Stack
    and its dependencies. Responsible for initalising the graph based on a set
    of Stacks.
    """

    def __init__(self, stacks):
        """
        Initialises a StackGraph based on a `set` of Stacks.

        :param stacks: A set of Stacks.
        :type stacks: set
        """
        self.logger = logging.getLogger(__name__)
        self.__graph = nx.DiGraph()
        self.__generate_graph(stacks)

    @property
    def graph(self):
        return self.__graph

    @graph.setter
    def graph(self, graph):
        self.__graph = graph

    def __repr__(self):
        return str(nx.convert.to_dict_of_lists(self.__graph))

    def __iter__(self):
        return self.__graph.__iter__()

    def __len__(self):
        return self.__graph.number_of_nodes()

    def filtered(self, source_stacks, reverse=False):
        graph = (nx.reverse if reverse else nx.DiGraph)(self.__graph)

        relevant = set(source_stacks)
        for stack in source_stacks:
            relevant |= nx.algorithms.dag.ancestors(graph, stack)
        graph.remove_nodes_from({stack for stack in graph if stack not in relevant})

        filtered = StackGraph(set())
        filtered.graph = graph

        return filtered

    def count_dependencies(self, stack):
        """
        Returns the number of incoming edges a given Stack has in the
        StackGraph. The number of incoming edge also represents the number
        of Stacks that depend on the given Stack.
        """
        return self.__graph.in_degree(stack)

    def remove_stack(self, stack):
        """
        Removes a Stack from the StackGraph. This operation will also remove
        all adjecent edges that represent a 'depends on' relationship with
        other Stacks.
        """
        return self.__graph.remove_node(stack)

    def filter_nodes(self, pattern):
        matched = set()
        for node in self.graph:
            if re.search(pattern, node.id):
                matched.add(node)
        return matched

    def __generate_graph(self, stacks):
        self.__graph.add_nodes_from(stacks)
        self.__generate_edges()

    def __generate_edges(self):
        for stack in self.__graph.copy().nodes():
            self.logger.debug(
                "Generate dependencies for stack {0}".format(stack)
            )

            if stack.config.dependencies:
                dep = stack.config.dependencies
                dep_node = self.__get_stack_from_graph_by_id(dep)
                self.__graph.add_edge(dep_node, stack)
                if not nx.is_directed_acyclic_graph(self.__graph):
                    raise CircularDependenciesError(
                        "Dependency cycle detected: {} {}".format(stack, dep))
                self.logger.debug("  Added dependency: {}".format(dep))

        self.__graph.remove_edges_from(nx.selfloop_edges(self.__graph))

    def __get_stack_from_graph_by_id(self, stack_id):
        for node in self.__graph.copy():
            if node.id == stack_id:
                return node
