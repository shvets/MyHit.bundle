import copy

from storage import Storage
from file_storage import FileStorage
from media_info import MediaInfo

class MediaInfoStorage(FileStorage):
    def __init__(self, file_name):
        FileStorage.__init__(self, file_name)

    def find(self, search_item):
        MediaInfoStorage.sanitize(search_item)

        found = None

        for item in self.data:
            mode = search_item.type

            if item['path'] == search_item['path']:
                if mode == MediaInfo.VIDEO or mode == MediaInfo.AUDIO:
                    if not 'season' in item:
                        found = item
                    break

                elif mode == MediaInfo.SEASON:
                    if 'season' in item:
                        if item['season'] == search_item['season']:
                            if not 'episode' in item:
                                found = item
                    break

                elif mode == MediaInfo.EPISODE:
                    if 'season' in item and 'season' in search_item:
                        if item['season'] == search_item['season']:
                            if 'episode' in item and 'episode' in search_item:
                                if item['episode'] == search_item['episode']:
                                    found = item
                    break

        return found

    def add(self, item):
        bookmark = self.find(item)

        if not bookmark:
            Storage.add(self, item)

            self.save()

    def remove(self, item):
        bookmark = self.find(item)

        if bookmark:
            Storage.remove(self, item)

            self.save()

    def load_storage(self):
        data = FileStorage.load_storage(self)

        return self.dict_to_media_info(data)

    def save_storage(self, data):
        FileStorage.save_storage(self, self.media_info_to_dict(data))

    def dict_to_media_info(self, data):
        new_data = []

        for item in data:
            new_item = copy.copy(item)

            type = new_item['type']

            del new_item['type']

            new_data.append(MediaInfo(type=type, **new_item))

        return new_data

    def media_info_to_dict(self, data):
        new_data = copy.copy(data)

        for item in new_data:
            item['type'] = item.type

        return new_data