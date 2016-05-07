import constants
from plex_storage import PlexStorage

class MyHitStorage(PlexStorage):
    def __init__(self, file_name):
        PlexStorage.__init__(self, Core.storage, file_name)

        self.load()

    def append_controls(self, oc, handler, item):
        bookmark = self.find(item)

        if bookmark:
            oc.add(DirectoryObject(
                key=Callback(handler, operation='remove', **item),
                title=unicode(L('Remove Bookmark')),
                thumb=R(constants.REMOVE_ICON)
            ))
        else:
            oc.add(DirectoryObject(
                key=Callback(handler, operation='add', **item),
                title=unicode(L('Add Bookmark')),
                thumb=R(constants.ADD_ICON)
            ))

