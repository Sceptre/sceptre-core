import logging

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
