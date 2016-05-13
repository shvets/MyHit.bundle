from my_hit_service import MyHitService

from my_hit_plex_storage import MyHitPlexStorage

class MyHitPlexService(MyHitService):
    def __init__(self):
        storage_name = Core.storage.abs_path(Core.storage.join_path(Core.bundle_path, 'Contents', 'myhit.storage'))

        self.queue = MyHitPlexStorage(storage_name)

        self.queue.register_simple_type('movie')
        self.queue.register_simple_type('track')
        self.queue.register_simple_type('serie')
        self.queue.register_simple_type('selection')
        self.queue.register_simple_type('tracks')
        self.queue.register_simple_type('soundtrack')
