class MediaInfo(dict):
    SIMPLE = 'simple'
    SEASON = 'season'
    EPISODE = 'episode'

    def __init__(self, type=SIMPLE, **params):
        super(MediaInfo, self).__init__()

        self.type = type

        for key, value in params.iteritems():
            self[key] = value

    def value(self, name):
        if name  in self:
            return self[name]
