# -*- coding: utf-8 -*-

import util
import history
import constants
from plex_service import PlexService

service = PlexService()

import main

def Start():
    Plugin.AddViewGroup("InfoList", viewMode="InfoList", mediaType="items")
    Plugin.AddViewGroup("List", viewMode="List", mediaType="items")
    Plugin.AddViewGroup('PanelStream', viewMode='PanelStream', mediaType='items')
    Plugin.AddViewGroup('MediaPreview', viewMode='MediaPreview', mediaType='items')

    DirectoryObject.art = R(constants.ART)
    VideoClipObject.art = R(constants.ART)

    HTTP.CacheTime = CACHE_1HOUR

    util.validate_prefs()

@handler(constants.PREFIX, 'MyHit', R(constants.ART), R(constants.ICON))
def MainMenu():
    if not service.available():
        return MessageContainer(L('Error'), L('Service not avaliable'))

    oc = ObjectContainer(title2=unicode(L('Title')), no_cache=True)

    oc.add(DirectoryObject(key=Callback(main.HandleAllMovies), title=unicode(L('Movies'))))
    oc.add(DirectoryObject(key=Callback(main.HandleAllSeries), title=unicode(L('Series'))))
    oc.add(DirectoryObject(key=Callback(main.HandlePopularMovies), title=unicode(L('Popular Movies'))))
    oc.add(DirectoryObject(key=Callback(main.HandlePopularSeries), title=unicode(L('Popular Series'))))
    oc.add(DirectoryObject(key=Callback(main.HandleSoundtracks), title=unicode(L('Soundtracks'))))
    oc.add(DirectoryObject(key=Callback(main.HandleSelections), title=unicode(L('Selections'))))
    oc.add(DirectoryObject(key=Callback(main.HandleHistory), title=unicode(L('History'))))
    oc.add(DirectoryObject(key=Callback(main.HandleQueue), title=unicode(L('Queue'))))

    oc.add(InputDirectoryObject(
        key=Callback(main.HandleSearch),
        title=unicode(L('Search')), prompt=unicode(L('Search on MyHit.org'))
    ))

    return oc
