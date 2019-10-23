import pytest

from sceptre.file_manager.file_data import FileData


class TestFileData:
    def test_file_data_instantiation_fails_with_invalid_path(self):
        with pytest.raises(OSError):
            FileData('path', 'data')

    def test_file_data_repr(self, tmpdir):
        path = tmpdir.mkdir("dummy_path").join('stack.yaml')
        path.write('data')
        fd = FileData(path, 'data')
        assert fd.__repr__() == \
            "sceptre.file_manager.file_data.FileData("\
            "'{}', " \
            "data"\
            ")".format(path)

    def test_file_data_str(self, tmpdir):
        path = tmpdir.mkdir("dummy_path").join('stack.yaml')
        path.write('data')
        fd = FileData(path, "hello")
        assert str(fd) == "path: {}, stream: {}".format(path, 'hello')

    def test_basename_return_correctly(self, tmpdir):
        path = tmpdir.mkdir("dummy_path").join('stack.yaml')
        path.write('data')
        fd = FileData(path, "data")
        assert fd.basename == 'stack.yaml'
