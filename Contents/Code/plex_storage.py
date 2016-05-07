import json

from file_storage import FileStorage

class PlexStorage(FileStorage):
    def __init__(self, storage, file_name):
        FileStorage.__init__(self, file_name)

        self.storage = storage

        self.clear()

    def exist(self):
        return self.storage.file_exists(self.file_name)

    def load_storage(self):
        return json.loads(self.storage.load(self.file_name))

    def save_storage(self, data):
        self.storage.save(self.file_name, json.dumps(self.data, indent=4))
