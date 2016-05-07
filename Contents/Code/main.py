# -*- coding: utf-8 -*-

import json
import constants
import util
import pagination
import history
from flow_builder import FlowBuilder

builder = FlowBuilder()

@route(constants.PREFIX + '/all_movies')
def HandleAllMovies(page=1):
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

    pagination.append_controls(oc, response, callback=HandleAllMovies, page=page)

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

    pagination.append_controls(oc, response, callback=HandlePopularMovies, page=page)

    return oc

@route(constants.PREFIX + '/movie')
def HandleMovie(path, name, thumb, parentName=None, season=None, episode=None, operation=None, container=False):
    oc = ObjectContainer(title2=unicode(L(name)))

    url_items = service.get_urls_with_metadata(path)

    if operation == 'add':
        service.queue.add_bookmark(path=path, name=name, thumb=thumb, season=season, episode=episode)
    elif operation == 'remove':
        service.queue.remove_bookmark(path=path, name=name, thumb=thumb, season=season, episode=episode)

    oc.add(MetadataObjectForURL(media_type="movie", path=path, name=name, thumb=thumb,
                                url_items=url_items, player=PlayVideo, parentName=parentName))

    if str(container) == 'False':
        history.push_to_history(path=path, name=name, thumb=thumb, parentName=parentName, season=season, episode=episode)
        service.queue.append_controls(oc, HandleMovie, path=path, name=name, thumb=thumb, parentName=parentName,
                                      season=season, episode=episode)

    return oc

@route(constants.PREFIX + '/all_series')
def HandleAllSeries(page=1):
    oc = ObjectContainer(title2=unicode(L('Series')))

    response = service.get_all_series(page=page)

    for item in response['movies']:
        name = item['name']
        path = item['path']
        thumb = item['thumb']

        oc.add(DirectoryObject(
            key=Callback(HandleSeasons, path=path, name=name, thumb=thumb),
            title=util.sanitize(name),
            thumb=thumb
        ))

    pagination.append_controls(oc, response, callback=HandleAllSeries, page=page)

    return oc

@route(constants.PREFIX + '/popular_series')
def HandlePopularSeries(page=1):
    oc = ObjectContainer(title2=unicode(L('Popular Series')))

    response = service.get_popular_series(page=page)

    for item in response['movies']:
        name = item['name']
        path = item['path']
        thumb = item['thumb']

        oc.add(DirectoryObject(
            key=Callback(HandleSeasons, path=path, name=name, thumb=thumb),
            title=util.sanitize(name),
            thumb=thumb
        ))

    pagination.append_controls(oc, response, callback=HandlePopularSeries, page=page)

    return oc

@route(constants.PREFIX + '/seasons')
def HandleSeasons(path, name, thumb, operation=None):
    oc = ObjectContainer(title2=unicode(L('Series')))

    if operation == 'add':
        service.queue.add_bookmark(path=path, name=name, thumb=thumb)
    elif operation == 'remove':
        service.queue.remove_bookmark(path=path, name=name, thumb=thumb)

    serie_info = service.get_serie_info(path)

    Log(serie_info)
    Log(len(serie_info))

    # for season in sorted(serial_info['seasons'].keys()):
    # # for item in response['movies']:
    #     name = item['name']
    #     path = item['path']
    #     thumb = item['thumb']
    #
    #     oc.add(SeasonObject(
    #         key=Callback(HandleEpisodes, path=path, name=name, thumb=thumb),
    #         title=util.sanitize(name),
    #         thumb=thumb
    #     ))
    #
    # service.queue.append_controls(oc, HandleSeasons, path=path, name=name, thumb=thumb)

    return oc

@route(constants.PREFIX + '/episodes', container=bool)
def HandleEpisodes(path, parentName, name, thumb, season, operation=None, container=False):
    oc = ObjectContainer(title2=unicode(parentName))

    if operation == 'add':
        service.queue.add_bookmark(path=path, parentName=parentName, name=name, thumb=thumb, season=season)
    elif operation == 'remove':
        service.queue.remove_bookmark(path=path, parentName=parentName, name=name, thumb=thumb, season=season)

    document = service.get_movie_document(path, season, 1)
    serial_info = service.get_serial_info(document)

    for episode in sorted(serial_info['episodes'].keys()):
        episode_name = serial_info['episodes'][episode]

        key = Callback(HandleMovie, path=path, title=episode_name, name=name,
                       thumb=thumb, season=season, episode=episode, container=container)

        oc.add(DirectoryObject(key=key, title=unicode(episode_name)))

    service.queue.append_controls(oc, HandleEpisodes, path=path, parentName=parentName, name=name, thumb=thumb, season=season)

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

    pagination.append_controls(oc, response, callback=HandleSoundtracks, page=page)

    return oc

@route(constants.PREFIX + '/soundtrack')
def HandleSoundtrack(path, name, thumb, audio=True, operation=None, container=False):
    oc = ObjectContainer(title2=unicode(name))

    if operation == 'add':
        service.queue.add_bookmark(path=path, name=name, thumb=thumb, audio=True)
    elif operation == 'remove':
        service.queue.remove_bookmark(path=path, name=name, thumb=thumb, audio=True)

    albums = service.get_albums(path)

    albums_count = len(albums)

    for index, album in enumerate(albums):
        prefix = str(index + 1) + ". " if albums_count > 1 else ""

        album_name = prefix + album['name']
        thumb = album['thumb']
        artist = album['composer']
        tracks = album['tracks']

        oc.add(DirectoryObject(
            key=Callback(HandleTracks, name=album_name, artist=artist, tracks=json.dumps(tracks)),
            title=util.sanitize(album_name),
            thumb=thumb
        ))

    if str(container) == 'False':
        history.push_to_history(path=path, name=name, thumb=thumb)
        service.queue.append_controls(oc, HandleSoundtrack, path=path, name=name, thumb=thumb, audio=audio)

    return oc

@route(constants.PREFIX + '/tracks')
def HandleTracks(name, artist, tracks):
    oc = ObjectContainer(title2=unicode(name))

    for track in json.loads(tracks):
        url = track['url']
        name = track['name']
        format = "mp3"
        bitrate = track['bitrate']
        duration = track['duration']

        oc.add(GetAudioTrack(path=url, name=unicode(name), artist=artist, format=format,
                             bitrate=bitrate, duration=duration))

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

    pagination.append_controls(oc, response, callback=HandleSelections, page=page)

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

    pagination.append_controls(oc, response, callback=HandleSelection, page=page, id=id, name=name)

    return oc

@route(constants.PREFIX + '/container')
def HandleContainer(path, parentName, name, thumb=None):
    if service.is_single_movie(path):
        return HandleMovie(path=path, name=name, thumb=thumb)
    else:
        return HandleSeasons(path=path, parentName=parentName, name=name, thumb=thumb)

@route(constants.PREFIX + '/search')
def HandleSearch(query=None, page=1):
    oc = ObjectContainer(title2=unicode(L('Search')))

    response = service.search(query=query, page=page)

    for movie in response['movies']:
        name = movie['name']
        thumb = movie['thumb']
        path = movie['path']

        oc.add(DirectoryObject(
            key=Callback(HandleContainer, path=path, parentName=name, name=name, thumb=thumb),
            title=unicode(name),
            thumb=thumb
        ))

    pagination.append_controls(oc, response, callback=HandleSearch, query=query, page=page)

    return oc

@route(constants.PREFIX + '/history')
def HandleHistory():
    history_object = history.load_history()

    oc = ObjectContainer(title2=unicode(L('History')))

    if history_object:
        for item in sorted(history_object.values(), key=lambda k: k['time'], reverse=True):
            path = item['path']
            name = item['name']

            if item['thumb']:
                thumb = service.get_thumb(item['thumb'])
            else:
                thumb = None

            oc.add(DirectoryObject(
                key=Callback(HandleContainer, path=path, parentName=name, name=name, thumb=thumb),
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
                key=Callback(HandleSeasons, **item),
                title=util.sanitize(item['name']),
                thumb=item['thumb']
            ))
        elif 'audio' in item:
            oc.add(DirectoryObject(
                key=Callback(HandleSoundtrack, **item),
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

@route(constants.PREFIX + '/audio_track')
def GetAudioTrack(path, name, artist, format, bitrate, duration, container=False):
    if 'm4a' in format:
        audio_container = Container.MP4
        audio_codec = AudioCodec.AAC
    else:
        audio_container = Container.MP3
        audio_codec = AudioCodec.MP3

    url_items = [
        {
            "url": path,
            "config": {
                "container": audio_container,
                "audio_codec": audio_codec,
                "bitrate": bitrate,
                "duration": duration,
            }
        }
    ]

    track = MetadataObjectForURL2(media_type="track", path=path, name=name, artist=artist, format=format,
                                  bitrate=bitrate, duration=duration, url_items=url_items, player=PlayAudio)

    if container:
        oc = ObjectContainer(title2=unicode(name))

        oc.add(track)

        return oc
    else:
        return track

def MetadataObjectForURL(media_type, path, name, thumb, url_items, player, parentName=None):
    metadata_object = builder.build_metadata_object(media_type=media_type, title=name)

    metadata_object.key = Callback(HandleMovie, path=path, name=name, thumb=thumb, parentName=parentName, container=True)

    # metadata_object.rating_key = 'rating_key'
    metadata_object.rating_key = unicode(name)
    # metadata_object.rating = data['rating']
    metadata_object.thumb = thumb
    # metadata_object.url = urls['m3u8'][0]
    # metadata_object.art = data['thumb']
    # metadata_object.tags = data['tags']
    # metadata_object.duration = data['duration'] * 1000
    # metadata_object.summary = data['summary']
    # metadata_object.directors = data['directors']

    metadata_object.items.extend(MediaObjectsForURL(url_items, player=player))

    return metadata_object

def MetadataObjectForURL2(media_type, path, name, artist, format, bitrate, duration, url_items, player):
    metadata_object = builder.build_metadata_object(media_type=media_type, title=name)

    metadata_object.key = Callback(GetAudioTrack, path=path, name=name, artist=artist,
                                   format=format, bitrate=bitrate, duration=duration, container=True)
    metadata_object.rating_key = unicode(name)
    metadata_object.duration = int(duration) * 1000
    metadata_object.artist = artist

    metadata_object.items.extend(MediaObjectsForURL(url_items, player))

    return metadata_object

def MediaObjectsForURL(url_items, player):
    media_objects = []

    for item in url_items:
        url = item['url']
        config = item['config']

        play_callback = Callback(player, url=url)

        media_object = builder.build_media_object(play_callback, config)

        media_objects.append(media_object)

    return media_objects

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

@route(constants.PREFIX + '/play_audio')
def PlayAudio(url):
    return Redirect(url)