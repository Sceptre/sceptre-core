import logging

from sceptre.provider.stack import StackConfigData
from sceptre.provider.stack import Stack


class SceptreCore:

    def __init__(self, stack_map):
        self.logger = logging.getLogger(__name__)
        self.stacks = self.__generate_stacks(stack_map)

    def __generate_stacks(self, stack_map):
        stacks = []
        for k, v in stack_map.items():
            stack_config = StackConfigData(v)
            stack = Stack(k, stack_config)
            stacks.append(stack)
        return stacks
