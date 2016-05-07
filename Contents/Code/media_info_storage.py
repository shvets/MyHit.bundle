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
            mode = search_item['type']

            if item['path'] == search_item['path']:
                if mode == MediaInfo.VIDEO or mode == MediaInfo.AUDIO or mode == MediaInfo.SELECTION:
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
        return FileStorage.load_storage(self)

    def save_storage(self, data):
        FileStorage.save_storage(self, data)

