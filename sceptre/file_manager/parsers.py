import logging
import yaml

from sceptre.exceptions import SceptreYamlError


class SceptreYamlParser(object):
    def __init__(self):
        self.logger = logging.getLogger(__name__)

    def load(self, stream):
        try:
            data = yaml.load(stream, Loader=yaml.FullLoader)
        except yaml.YAMLError:
            raise SceptreYamlError(
                "The stream {} could not be parsed.".format(stream))
        return data
