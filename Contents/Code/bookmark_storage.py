from file_storage import FileStorage

class BookmarkStorage(FileStorage):
    def __init__(self, file_name):
        FileStorage.__init__(self, file_name)

    def add_bookmark(self, item):
        bookmark = self.get_bookmark(item)

        if not bookmark:
            self.add(item)

            self.save()

    def remove_bookmark(self, item):
        self.remove(item)

        self.save()

    def get_bookmark(self, item):
        if 'season' in item and not item['season']:
            del (item['season'])

        if 'episode' in item and not item['episode']:
            del (item['episode'])

        if 'parentName' in item and not item['parentName']:
            del (item['parentName'])

        found = None

        for item in self.data:
            if 'path' in item:
                if 'path' in item and item['path'] == item['path']:
                    if 'season' in item:
                        if 'season' in item and item['season'] == item['season']:
                            if 'episode' in item:
                                if 'episode' in item and item['episode'] == item['episode']:
                                    found = item
                                    break
                            else:
                                found = item
                                break
                    else:
                        found = item
                        break

        return found