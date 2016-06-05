import plex_util
from flow_builder import FlowBuilder

from my_hit_plex_service import MyHitPlexService

service = MyHitPlexService()

def MediaObjectsForURL(urls, player):
    media_objects = []

    for url, config in urls.iteritems():
        play_callback = Callback(player, url=url)

        media_object = FlowBuilder.build_media_object(play_callback, config)

        media_objects.append(media_object)

    return media_objects

@indirect
@route(PREFIX + '/play_video')
def PlayVideo(url, play_list=True):
    if not url:
        return plex_util.no_contents()
    else:
        if str(play_list) == 'True':
            url = Callback(PlayList, url=url)

        return IndirectResponse(MovieObject, key=RTMPVideoURL(url))

@route(PREFIX + '/play_list.m3u8')
def PlayList(url):
    play_list = service.get_play_list(url)

    return play_list

@route(PREFIX + '/play_audio')
def PlayAudio(url):
    return Redirect(url)
