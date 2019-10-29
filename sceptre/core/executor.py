# -*- coding: utf-8 -*-

"""
sceptre.plan.executor

This module implements a SceptrePlanExecutor, which is responsible for
executing the command specified in a SceptrePlan.
"""
import logging

from concurrent.futures import ThreadPoolExecutor, as_completed
from sceptre.provider.stack_status import StackStatus


class Executor:

    def __init__(self, command, execute_order):
        """
        Initalises a Executor, generates the execute order, threads
        and intial Stack Statuses.

        :param command: The command to execute on the Stack.
        :type command: str

        :param execute_order: A list containing sets of Stacks that can be\
                executed concurrently.
        :type execute_order: list
        """

        self.logger = logging.getLogger(__name__)
        self.command = command
        self.execute_order = execute_order

        self.num_threads = len(max(execute_order, key=len))
        self.stack_statuses = {stack: StackStatus.PENDING
                               for batch in execute_order for stack in batch}

    def execute(self, *args):
        """
        Execute is responsible executing the sets of Stacks in `execute_order`
        concurrently, in the correct order.

        :param args: Any arguments that should be passed through to the\
                StackAction being called.
        """
        responses = {}
        with ThreadPoolExecutor(max_workers=self.num_threads) as executor:
            for batch in self.execute_order:
                futures = [executor.submit(self._execute, stack, *args)
                           for stack in batch]
                for future in as_completed(futures):
                    stack, status = future.result()
                    responses[stack] = status
        return responses

    def _execute(self, stack, *args):
        result = getattr(stack, self.command)(*args)
        return stack, result
