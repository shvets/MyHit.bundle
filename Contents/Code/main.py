# -*- coding: utf-8 -*-

import constants
import util
import pagination
import history
from flow_builder import FlowBuilder

builder = FlowBuilder()

@route(constants.PREFIX + '/movies')
def HandleMovies(page=1):
    oc = ObjectContainer(title2=unicode(L('Movies')))

    response = service.get_all_movies(page=page)

    for item in response['movies']:
        name = item['name']
        path = item['path']
        thumb = item['thumb']

        oc.add(DirectoryObject(
            key=Callback(HandleMovie, path=path, name=name, thumb=thumb),
            title=util.sanitize(name),
            thumb=thumb
        ))

    pagination.append_controls(oc, response, page=int(page), callback=HandleMovies)

    return oc

@route(constants.PREFIX + '/popular_movies')
def HandlePopularMovies(page=1):
    oc = ObjectContainer(title2=unicode(L('Popular Movies')))

    response = service.get_popular_movies(page=page)

    for item in response['movies']:
        name = item['name']
        path = item['path']
        thumb = item['thumb']

        oc.add(DirectoryObject(
            key=Callback(HandleMovie, path=path, name=name, thumb=thumb),
            title=util.sanitize(name),
            thumb=thumb
        ))

    pagination.append_controls(oc, response, page=int(page), callback=HandlePopularMovies)

    return oc

@route(constants.PREFIX + '/movie')
def HandleMovie(path, name, thumb, container=False):
    oc = ObjectContainer(title2=unicode(L(name)))

    urls = service.get_urls(path)

    # if operation == 'add':
    #     service.queue.add_bookmark(path=path, title=title, name=name, thumb=thumb, season=season, episode=episode)
    # elif operation == 'remove':
    #     service.queue.remove_bookmark(path=path, title=title, name=name, thumb=thumb, season=season, episode=episode)

    oc.add(MetadataObjectForURL(path=path, name=name, thumb=thumb, urls=urls))

    # if str(container) == 'False':
    #     history.push_to_history(path=path, title=title, name=name, thumb=thumb, season=season, episode=episode)
    #     service.queue.append_controls(oc, HandleMovie, path=path, title=title, name=name, thumb=thumb, season=season,
    #                                   episode=episode)

    return oc

@route(constants.PREFIX + '/all_serials')
def HandleSerials(page=1):
    oc = ObjectContainer(title2=unicode(L('Serials')))

    response = service.get_all_serials(page=page)

    for item in response['movies']:
        name = item['name']
        path = item['path']
        thumb = item['thumb']

        oc.add(DirectoryObject(
            key=Callback(HandleSerial, path=path, name=name, thumb=thumb),
            title=util.sanitize(name),
            thumb=thumb
        ))

    pagination.append_controls(oc, response, page=int(page), callback=HandleSerials)

    return oc

@route(constants.PREFIX + '/popular_serials')
def HandlePopularSerials(page=1):
    oc = ObjectContainer(title2=unicode(L('Popular Serials')))

    response = service.get_popular_serials(page=page)

    for item in response['movies']:
        name = item['name']
        path = item['path']
        thumb = item['thumb']

        oc.add(DirectoryObject(
            key=Callback(HandleSerial, path=path, name=name, thumb=thumb),
            title=util.sanitize(name),
            thumb=thumb
        ))

    pagination.append_controls(oc, response, page=int(page), callback=HandlePopularSerials)

    return oc

@route(constants.PREFIX + '/serial')
def HandleSerial(path, name, thumb, container=False):
    oc = ObjectContainer(title2=unicode(L(name)))

    urls = service.get_urls(path)

    # if operation == 'add':
    #     service.queue.add_bookmark(path=path, title=title, name=name, thumb=thumb, season=season, episode=episode)
    # elif operation == 'remove':
    #     service.queue.remove_bookmark(path=path, title=title, name=name, thumb=thumb, season=season, episode=episode)

    oc.add(MetadataObjectForURL(path=path, name=name, thumb=thumb, urls=urls))

    # if str(container) == 'False':
    #     history.push_to_history(path=path, title=title, name=name, thumb=thumb, season=season, episode=episode)
    #     service.queue.append_controls(oc, HandleMovie, path=path, title=title, name=name, thumb=thumb, season=season,
    #                                   episode=episode)

    return oc

@route(constants.PREFIX + '/soundtracks')
def HandleSoundtracks(page=1):
    oc = ObjectContainer(title2=unicode(L('Soundtracks')))

    response = service.get_soundtracks(page=page)

    for item in response['movies']:
        name = item['name']
        path = item['path']
        thumb = item['thumb']

        oc.add(DirectoryObject(
            key=Callback(HandleSoundtrack, path=path, name=name, thumb=thumb),
            title=util.sanitize(name),
            thumb=thumb
        ))

    pagination.append_controls(oc, response, page=int(page), callback=HandleSoundtracks)

    return oc

@route(constants.PREFIX + '/soundtrack')
def HandleSoundtrack(path, name, thumb, container=False):
    oc = ObjectContainer(title2=unicode(L('Soundtracks')))

    albums = service.get_albums(path)

    Log(albums)

    for item in albums:
        album = item[0]['album']
        track = item[0]['track']
        url = item[0]['url']

        oc.add(DirectoryObject(
            key=Callback(GetAudioTrack, title='title', thumb='thumb', artist='artist', format='format', url=url, container=True),
            title=util.sanitize(name),
            thumb=thumb
        ))

    return oc

@route(constants.PREFIX + '/selections')
def HandleSelections(page=1):
    oc = ObjectContainer(title2=unicode(L('Selections')))

    response = service.get_selections(page=page)

    for item in response['movies']:
        name = item['name']
        id = item['id']
        thumb = item['thumb']

        if name != "Актёры и актрисы":
            oc.add(DirectoryObject(
                key=Callback(HandleSelection, id=id, name=name),
                title=util.sanitize(name),
                thumb=thumb
            ))

    pagination.append_controls(oc, response, page=int(page), callback=HandleSelections)

    return oc

@route(constants.PREFIX + '/selection')
def HandleSelection(id, name, page=1):
    oc = ObjectContainer(title2=unicode(name))

    response = service.get_selection(id, page=page)

    for item in response['movies']:
        name = item['name']
        path = item['path']
        thumb = item['thumb']

        oc.add(DirectoryObject(
            key=Callback(HandleMovie, path=path, name=name, thumb=thumb),
            title=util.sanitize(name),
            thumb=thumb
        ))

    pagination.append_controls(oc, response, page=int(page), callback=HandleSelection)

    return oc

def MetadataObjectForURL(path, name, thumb, urls):
    params = {}

    # document = service.fetch_document(path)
    # data = service.get_media_data(document)
    #
    # if episode:
    #     media_type = 'episode'
    #     params['index'] = int(episode)
    #     params['season'] = int(season)
    #     params['content_rating'] = data['rating']
    #     # show=show,
    # else:
    #     media_type = 'movie'
    #     params['year'] = data['year']
    #     params['genres'] = data['genres']
    #     params['countries'] = data['countries']
    #     params['genres'] = data['genres']
    #     # video.tagline = 'tagline'
    #     # video.original_title = 'original_title'

    video = builder.build_metadata_object(media_type='movie', **params)

    video.title = name
    video.rating_key = 'rating_key'
    # video.rating = data['rating']
    video.thumb = thumb
    # video.url = urls['m3u8'][0]
    # video.art = data['thumb']
    # video.tags = data['tags']
    # video.duration = data['duration'] * 1000
    # video.summary = data['summary']
    # video.directors = data['directors']

    video.key = Callback(HandleMovie, path=path, name=name, thumb=thumb, container=True)

    video.items.extend(MediaObjectsForURL(urls))

    return video

def MediaObjectsForURL(urls):
    items = []

    for index, url in enumerate(reversed(urls)):
        metadata = service.get_metadata(url)

        play_callback = Callback(PlayVideo, url=url)

        media_object = builder.build_media_object(play_callback, play_list=True,
                                                  width=metadata['width'],
                                                  height=metadata['height'],
                                                  video_resolution=metadata['height'],
                                                  bitrate=metadata['bitrate'])

        items.append(media_object)

    return items

@route(constants.PREFIX + '/search')
def HandleSearch(query=None, page=1):
    oc = ObjectContainer(title2=unicode(L('Search')))

    response = service.search(query=query)

    for movie in response['movies']:
        name = movie['name']
        thumb = movie['thumb']
        path = movie['path']

        oc.add(DirectoryObject(
            key=Callback(HandleContainer, path=path, title=name, name=name, thumb=thumb),
            title=unicode(name),
            thumb=thumb
        ))

    pagination.append_controls(oc, response, page=page, callback=HandleSearch, query=query)

    return oc

@route(constants.PREFIX + '/history')
def HandleHistory():
    history_object = history.load_history()

    oc = ObjectContainer(title2=unicode(L('History')))

    if history_object:
        for item in sorted(history_object.values(), key=lambda k: k['time'], reverse=True):
            path = item['path']
            name = item['title']

            if item['thumb']:
                thumb = service.get_thumb(item['thumb'])
            else:
                thumb = None

            oc.add(DirectoryObject(
                key=Callback(HandleContainer, path=path, title=name, name=name, thumb=thumb),
                title=unicode(name),
                thumb=thumb
            ))

    return oc

@route(constants.PREFIX + '/queue')
def HandleQueue():
    oc = ObjectContainer(title2=unicode(L('Queue')))

    for item in service.queue.data:
        if 'episode' in item:
            oc.add(DirectoryObject(
                key=Callback(HandleMovie, **item),
                title=util.sanitize(item['name']),
                thumb=item['thumb']
            ))
        elif 'season' in item:
            oc.add(DirectoryObject(
                key=Callback(HandleEpisodes, **item),
                title=util.sanitize(item['name']),
                thumb=item['thumb']
            ))
        else:
            oc.add(DirectoryObject(
                key=Callback(HandleContainer, **item),
                title=util.sanitize(item['name']),
                thumb=item['thumb']
            ))

    return oc

@indirect
@route(constants.PREFIX + '/play_video')
def PlayVideo(url, play_list=True):
    if not url:
        return util.no_contents()
    else:
        if str(play_list) == 'True':
            url = Callback(PlayList, url=url)

        return IndirectResponse(MovieObject, key=RTMPVideoURL(url))

@route(constants.PREFIX + '/play_list.m3u8')
def PlayList(url):
    play_list = service.get_play_list(url)

    return play_list


@route(constants.PREFIX + '/audio_track')
def GetAudioTrack(title, thumb, artist, format, url, container=False, **params):
    track = MetadataObjectForURL2(title=title, thumb=thumb, artist=artist, format=format, url=url, container=container)

    if container:
        oc = ObjectContainer(title2=unicode(title))

        oc.add(track)

        return oc
    else:
        return track

def MetadataObjectForURL2(title, thumb, artist, format, url, container):
    track = TrackObject(
        key=Callback(GetAudioTrack, title=title, thumb=thumb, format=format, artist=artist, url=url, container=True),
        rating_key = unicode(title),
        title = unicode(title),
        # album = 'album',
        thumb=thumb,
        artist = artist
    )

    track.items = MediaObjectsForURL2(url, format)

    return track

def MediaObjectsForURL2(url, format):
    if 'm4a' in format:
        container = Container.MP4
        audio_codec = AudioCodec.AAC
    else:
        container = Container.MP3
        audio_codec = AudioCodec.MP3

    media_objects = []

    media_object = MediaObject(
        container = container,
        optimized_for_streaming=True
    )

    part_object = PartObject(key=Callback(PlayMusic, url=url))

    audio_stream = AudioStreamObject(codec=audio_codec, channels=2, bitrate=str(128))

    part_object.streams = [audio_stream]

    media_object.parts.append(part_object)

    media_objects.append(media_object)

    return media_objects

@route('/music/music/play_audio')
def PlayMusic(url):
    Log(url)

    return Redirect(url)