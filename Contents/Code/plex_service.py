from my_hit_service import MyHitService

from plex_storage import PlexStorage

class PlexService(MyHitService):
    def __init__(self):
        storage_name = Core.storage.abs_path(Core.storage.join_path(Core.bundle_path, 'Contents', 'myhit.storage'))

        self.queue = PlexStorage(storage_name)
