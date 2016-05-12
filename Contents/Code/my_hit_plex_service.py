from my_hit_service import MyHitService

from my_hit_storage import MyHitStorage

class MyHitPlexService(MyHitService):
    def __init__(self):
        storage_name = Core.storage.abs_path(Core.storage.join_path(Core.bundle_path, 'Contents', 'myhit.storage'))

        self.queue = MyHitStorage(storage_name)
