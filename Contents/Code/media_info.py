class MediaInfo(dict):
    SEASON = 'season'
    EPISODE = 'episode'
    TRACK = 'audio'
    SELECTION = 'selection'
    MOVIE = 'selection'

    def __init__(self, type, **params):
        super(MediaInfo, self).__init__()

        self['type'] = type

        for key, value in params.iteritems():
            self[key] = value
