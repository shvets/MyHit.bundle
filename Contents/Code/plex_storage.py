import json

from media_info_storage import MediaInfoStorage

class PlexStorage(MediaInfoStorage):
    def __init__(self, storage, file_name):
        MediaInfoStorage.__init__(self, file_name)

        self.storage = storage

        self.clear()

    def exist(self):
        return self.storage.file_exists(self.file_name)

    def load_storage(self):
        return self.dict_to_media_info(json.loads(self.storage.load(self.file_name)))

    def save_storage(self, data):
        self.storage.save(self.file_name, json.dumps(self.media_info_to_dict(self.data), indent=4))
