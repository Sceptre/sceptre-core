import copy
import fnmatch
import logging
import re
import os


from sceptre.file_manager.file_handler import FileHandler
from sceptre.file_manager import strategies


class FileManager:
    def __init__(self, context):
        self.logger = logging.getLogger(__name__)
        self.file_handler = FileHandler()
        self.context = context
        self.all_stacks = self.__get_all_stacks()
        self.command_stacks = self.__get_command_stacks()

    def __get_all_stacks(self):
        stacks = {}
        for stack_path in self.__get_all_stack_paths():
            stack_config = self.__generate_stack_config(stack_path)
            variables = {
                "var": self.context.user_variables,
                "stack_config": stack_config,
                "command_path": self.context.command_path,
            }
            opened_stack = self.file_handler.open(stack_path)
            rendered_stack = self.file_handler.render(
                opened_stack, variables=variables)
            parsed_stack = self.file_handler.parse(rendered_stack)
            parsed_stack.stream["stack_config"] = stack_config
            stacks.update({parsed_stack.path: parsed_stack.stream})
        return stacks

    def __get_command_stacks(self):
        command_stacks = {}
        for path, config in self.all_stacks.items():
            if path.startswith(self.context.full_command_path):
                command_stacks.update({path: config})
        return command_stacks

    def __get_all_stack_paths(self):
        return self.__walk(self.context.full_config_path, '^(?!config.|\\.).*')

    def __generate_stack_config(self, stack_path):
        config = self.__resolve_base_config()
        root = os.path.dirname(stack_path)

        if root == self.context.full_config_path:
            return config

        for path in self.__walk(root, "^config."):
            current_stream = self.file_handler.open(path)
            current_config = self.file_handler.parse(current_stream)
            config = self.__merge_config(config, current_config.stream)

        return config

    def __walk(self, root, pattern):
        items = []
        for directory_name, sub_directories, files in os.walk(
                root, topdown=False, followlinks=True):
            for filename in fnmatch.filter(files, '*.yaml'):
                if re.match(pattern, filename):
                    items.append(os.path.join(directory_name, filename))
        return items

    def __resolve_base_config(self):
        config = {}
        config_path = os.path.join(
            self.context.full_config_path, self.context.config_path)
        if os.path.exists(config_path):
            fd = self.file_handler.open(config_path)
            config = self.file_handler.parse(fd).stream
        return config

    def __merge_config(self, existing, current):
        STRATEGIES = {
            list: strategies.list_join,
            dict: strategies.dict_merge,
            str: strategies.child_wins,
            object: strategies.child_wins
        }

        existing_config = copy.deepcopy(existing)
        current_config = copy.deepcopy(current)
        for k, v in copy.deepcopy(existing_config).items():
            for t, strategy in STRATEGIES.items():
                if type(v) == t:
                    value = strategy(existing_config.get(k), current_config.get(k))
                    if value:
                        current_config[k] = value

        existing_config.update(current_config)
        return existing_config
