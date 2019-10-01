import os


class FileData(object):
    def __init__(self, path, stream):
        if os.path.isfile(path):
            self.path = path
        else:
            raise OSError('The path supplied to FileData is not a valid file path.')
        self.stream = stream

    def __repr__(self):
        return ("sceptre.file_manager.file_data.FileData("
                "'{path}', "
                '{stream}'
                ")".format(path=self.path, stream=self.stream)
                )

    def __str__(self):
        return "path: {}, stream: {}".format(self.path, self.stream)
