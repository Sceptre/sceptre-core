import logging

from sceptre.exceptions import ConfigFileNotFoundError
from sceptre.provider.stack import StackConfigData
from sceptre.provider.stack import Stack
from sceptre.core.graph import StackGraph
from sceptre.core.executor import Executor


class SceptreCore:

    def __init__(self, stack_map, execute_pattern, context):
        self.logger = logging.getLogger(__name__)
        self.__execute_pattern = execute_pattern
        self.context = context
        self.stacks = self.__generate_stacks(stack_map)
        self.graph = StackGraph(self.stacks)
        self.execute_stacks = self.graph.filter_nodes(execute_pattern)
        self.execute_order = self.__generate_execution_order()

    def execute(self, command):
        executor = Executor(command, self.execute_order)
        executor.execute()

    def __generate_stacks(self, stack_map):
        stacks = set()
        for stack_id, config in stack_map.items():
            stack_config = StackConfigData(config)
            stack = Stack(stack_id, stack_config)
            stacks.add(stack)
        return stacks

    def __generate_execution_order(self, reverse=False):
        if self.context.ignore_dependencies:
            return [self.execute_stacks]

        graph = self.graph.filtered(self.execute_stacks, reverse)

        execute_order = []
        while graph.graph:
            batch = set()
            for stack in graph:
                if graph.count_dependencies(stack) == 0:
                    batch.add(stack)
            execute_order.append(batch)

            for stack in batch:
                graph.remove_stack(stack)

        if not execute_order:
            raise ConfigFileNotFoundError(
                "No stacks detected from the given patterns'{}'. Valid stack patterns are: {}"
                .format(self.__execute_pattern, [item.id for item in self.stacks])
            )

        return execute_order
