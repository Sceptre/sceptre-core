import pytest

from sceptre.exceptions import SceptreYamlError

from sceptre.file_manager.parsers import SceptreYamlParser


class TestSceptreYamlParser(object):
    def test_load_yaml_file(self):
        parser = SceptreYamlParser()
        stream = """---
keyA: itemA
listA:
  - item1
  - item2
  - item3
"""
        yaml = parser.load(stream)
        assert yaml == {"keyA": "itemA", "listA": ["item1", "item2", "item3"]}

    def test_load_fails_with_invalid_yaml_raises_error(self):
        parser = SceptreYamlParser()
        stream = """
>>>>
key1: item1
"""
        with pytest.raises(SceptreYamlError):
            parser.load(stream)
