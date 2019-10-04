import copy
import fnmatch
import logging
import re
import os


from sceptre.file_manager.file_handler import FileHandler
from sceptre.file_manager import strategies

STRATEGIES = {
    'dependencies': strategies.list_join,
    'hooks': strategies.child_wins,
    'notifications': strategies.child_wins,
    'on_failure': strategies.child_wins,
    'parameters': strategies.child_wins,
    'profile': strategies.child_wins,
    'project_code': strategies.child_wins,
    'protect': strategies.child_wins,
    'region': strategies.child_wins,
    'required_version': strategies.child_wins,
    'role_arn': strategies.child_wins,
    'sceptre_user_data': strategies.child_wins,
    'stack_name': strategies.child_wins,
    'stack_tags': strategies.child_wins,
    'stack_timeout': strategies.child_wins,
    'template_bucket_name': strategies.child_wins,
    'template_key_value': strategies.child_wins,
    'template_path': strategies.child_wins
}


class FileManager(object):
    def __init__(self, context):
        self.logger = logging.getLogger(__name__)
        self.file_handler = FileHandler()
        self.context = context
        self.all_stacks = self.__get_all_stacks()

    def __get_all_stacks(self):
        stacks = {}
        for stack_path in self.__get_all_stack_paths():
            stack_config = self.__generate_stack_config(stack_path)
            variables = {"stack_config": stack_config}
            opened_stack = self.file_handler.open(stack_path)
            rendered_stack = self.file_handler.render(opened_stack, self.context, vars=variables)
            parsed_stack = self.file_handler.parse(rendered_stack)
            parsed_stack.stream["stack_config"] = stack_config
            stacks.update({parsed_stack.path: parsed_stack.stream})
        return stacks

    def __get_all_stack_paths(self):
        if self.context.ignore_dependencies:
            root = self.context.full_command_path
        else:
            root = self.context.full_config_path

        if os.path.isfile(root):
            return {root}

        return self.__walk(root, '^(?!config.|\\.).*')

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
        existing_config = copy.deepcopy(existing)
        current_config = copy.deepcopy(current)
        for key, strategy in STRATEGIES.items():
            value = strategy(existing_config.get(key), current_config.get(key))
            if value:
                current_config[key] = value
            existing_config.update(current_config)
        return existing_config
