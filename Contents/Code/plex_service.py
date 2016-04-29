from my_hit_service import MyHitService

from plex_storage import PlexStorage

class PlexService(MyHitService):
    def __init__(self):
        storage_name = Core.storage.abs_path(Core.storage.join_path(Core.bundle_path, 'Contents', 'myhit.storage'))

        self.queue = PlexStorage(storage_name)

    # def load_cache(self, path):
    #     if Data.Exists(self.KEY_CACHE):
    #         ret = Data.LoadObject(self.KEY_CACHE)
    #
    #         if ret and 'path' in ret and ret['path'] == path:
    #             Log.Debug('Return from cache %s' % path)
    #
    #             return ret
    #
    # def save_cache(self, data):
    #     Data.SaveObject(self.KEY_CACHE, data)