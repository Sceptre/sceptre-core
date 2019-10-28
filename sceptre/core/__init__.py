import logging

from sceptre.provider.stack import StackConfigData
from sceptre.provider.stack import Stack
from sceptre.core.graph import StackGraph


class SceptreCore:

    def __init__(self, stack_map):
        self.logger = logging.getLogger(__name__)
        self.stacks = self.__generate_stacks(stack_map)
        self.graph = StackGraph(self.stacks)

    def __generate_stacks(self, stack_map):
        stacks = set()
        for k, v in stack_map.items():
            stack_config = StackConfigData(v)
            stack = Stack(k, stack_config)
            stacks.add(stack)
        return stacks
