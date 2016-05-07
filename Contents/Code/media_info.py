class MediaInfo(dict):
    VIDEO = 'video'
    AUDIO = 'audio'
    SERIE = 'serie'
    SEASON = 'season'
    EPISODE = 'episode'
    SELECTION = 'selection'

    def __init__(self, type=VIDEO, **params):
        super(MediaInfo, self).__init__()

        self['type'] = type

        for key, value in params.iteritems():
            self[key] = value

    def value(self, name):
        if name  in self:
            return self[name]
