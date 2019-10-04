import logging
import os

import jinja2

from sceptre.exceptions import SceptreYamlError

from sceptre.file_manager.file_data import FileData
from sceptre.file_manager.parsers import SceptreYamlParser


class FileHandler(object):

    def __init__(self):
        self.logger = logging.getLogger(__name__)

    def open(self, path):
        try:
            with open(path) as f:
                stream = f.read()
        except FileNotFoundError:
            raise FileNotFoundError("Could not find file {}".format(path))

        return FileData(path, stream)

    def parse(self, file_data):
        parser = SceptreYamlParser()
        try:
            yaml = parser.load(file_data.stream)
        except SceptreYamlError:
            raise SceptreYamlError(
                "There was a problem parsing the stream {}".format(file_data.path)
            )
        parsed = FileData(file_data.path, yaml)
        return parsed

    def render(self, file_data, context, vars={}):
        template_vars = {"var": context.user_variables}
        for k, v in vars.items():
            template_vars.update({k: v})

        jinja_env = jinja2.Environment(
            loader=jinja2.FileSystemLoader(file_data.dirname),
            undefined=jinja2.StrictUndefined
        )

        template = jinja_env.get_template(file_data.basename)
        rendered = template.render(
            template_vars,
            command_path=context.command_path.split(os.path.sep),
            environment_variable=os.environ
        )

        return FileData(file_data.path, rendered)
