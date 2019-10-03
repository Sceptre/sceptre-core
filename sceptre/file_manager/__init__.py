import fnmatch
import logging
import os

from sceptre.file_manager.file_handler import FileHandler


class FileManager(object):
    def __init__(self, context):
        self.logger = logging.getLogger(__name__)
        self.context = context
        self.all_stacks = self.__get_all_stacks()

    def __get_all_stacks(self):
        stacks = {}
        file_handler = FileHandler()
        discovered_stacks = self.__discover_stack_paths()
        for stack_path in discovered_stacks:
            opened = file_handler.open(stack_path)
            rendered = file_handler.render(opened, self.context)
            parsed = file_handler.parse(rendered)
            stacks.update({parsed.path: parsed.stream})
        return stacks

    def __discover_stack_paths(self):
        stack_paths = set()
        if self.context.ignore_dependencies:
            root = self.context.full_command_path
        else:
            root = self.context.full_config_path
        if os.path.isfile(root):
            stack_paths = {root}
        else:
            for directory_name, sub_directories, files in os.walk(root, followlinks=True):
                for filename in fnmatch.filter(files, '*.yaml'):
                    if filename.startswith('config.'):
                        continue
                    stack_paths.add(os.path.join(directory_name, filename))
        return stack_paths
