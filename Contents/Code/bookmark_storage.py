from storage import Storage
from file_storage import FileStorage
from media_info import MediaInfo

class BookmarkStorage(FileStorage):
    def __init__(self, file_name):
        FileStorage.__init__(self, file_name)

    def sanitize(self, item):
        new_item = MediaInfo(item.type)

        for key, value in item.iteritems():
            if item[key]:
                new_item[key] = value

        return new_item

    def find(self, search_item):
        search_item = self.sanitize(search_item)

        found = None

        for item in self.data:
            mode = search_item.type()

            if item['path'] == search_item['path']:
                if mode == MediaInfo.SIMPLE:
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
        Storage.remove(self, item)

        self.save()