from plex_storage import PlexStorage

class MyHitPlexStorage(PlexStorage):
    def __init__(self, file_name):
        PlexStorage.__init__(self, Core.storage, file_name)

        self.load()


