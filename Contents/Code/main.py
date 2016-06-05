# -*- coding: utf-8 -*-

import json
import common_routes
from collections import OrderedDict
import plex_util
import pagination
import history
from flow_builder import FlowBuilder
from media_info import MediaInfo

# import sys
#
# for path in sys.path:
#     Log(path)

@route(PREFIX + '/all_movies')
def HandleAllMovies(page=1):
    return HandleMovies("/film/", title='Movies', page=page)

@route(PREFIX + '/popular_movies')
def HandlePopularMovies(page=1):
    return HandleMovies("/film/?s=3", title='Popular Movies', page=page)

@route(PREFIX + '/movies')
def HandleMovies(path, title, page=1):
    oc = ObjectContainer(title2=unicode(L(title)))

    response = service.get_movies(path=path, page=page)

    for item in response['movies']:
        name = item['name']
        thumb = item['thumb']

        new_params = {
            'type': "movie",
            'id' :item['path'],
            'name': item['name'],
            'thumb': item['thumb']
        }
        oc.add(DirectoryObject(
            key=Callback(HandleMovie, **new_params),
            title=plex_util.sanitize(name),
            thumb=plex_util.get_thumb(thumb)
        ))

    pagination.append_controls(oc, response, callback=HandleMovies, path=path, title=title, page=page)

    return oc

def build_urls_with_metadata(media_info):
    if 'season' in media_info:
        season = media_info['season']
    else:
        season = None

    if 'episode' in media_info:
        episode = media_info['episode']
    else:
        episode = None

    if season and int(season) > 0 and episode:
        urls = service.get_urls(url=media_info['id'])
    else:
        urls = service.get_urls(path=media_info['id'])

    urls_with_metadata = OrderedDict()

    for url in urls:
        metadata = service.get_metadata(url)

        # config = FlowBuilder.get_plex_config(format)
        config = {}

        config["width"] = metadata['width']
        config["height"] = metadata['height']
        config["video_resolution"] = metadata['height']
        config["bitrate"] = metadata['bitrate']
        #config["duration"] = media_info['duration']

        urls_with_metadata[url] = config

    return urls_with_metadata

@route(PREFIX + '/movie')
def HandleMovie(operation=None, container=False, **params):
    oc = ObjectContainer(title2=unicode(L(params['name'])))

    media_info = MediaInfo(**params)

    media_data = service.get_media_data(media_info['id'])

    url_items = build_urls_with_metadata(media_info)

    if len(url_items.keys()) == 0:
        return plex_util.no_contents()
    else:
        service.queue.handle_bookmark_operation(operation, media_info)

        metadata_object = FlowBuilder.build_metadata_object(media_type=media_info['type'], title=media_info['name'])

        metadata_object.key = Callback(HandleMovie, container=True, **media_info)

        metadata_object.rating_key = unicode(media_info['name'])
        metadata_object.thumb = media_info['thumb']
        metadata_object.title = media_info['name']
        metadata_object.tags = media_data['tags']
        metadata_object.duration = media_data['duration']
        metadata_object.summary = media_data['description']
        metadata_object.directors = media_data['directors']

        metadata_object.items.extend(common_routes.MediaObjectsForURL(url_items, player=common_routes.PlayVideo))

        oc.add(metadata_object)

        if str(container) == 'False':
            history.push_to_history(Data, media_info)
            service.queue.append_bookmark_controls(oc, HandleMovie, media_info)

        return oc

@route(PREFIX + '/all_series')
def HandleAllSeries(page=1):
    return HandleSeries("/serial/", title='Series', page=page)

@route(PREFIX + '/popular_series')
def HandlePopularSeries(page=1):
    return HandleSeries("/serial/?s=3", title='Popular Series', page=page)

@route(PREFIX + '/series')
def HandleSeries(path, title, page=1):
    oc = ObjectContainer(title2=unicode(L(title)))

    response = service.get_series(path=path, page=page)

    for item in response['movies']:
        new_params = {
            'type': 'serie',
            'id': item['path'],
            'name': item['name'],
            'thumb': item['thumb']
        }

        oc.add(DirectoryObject(
            key=Callback(HandleSerie, **new_params),
            title=plex_util.sanitize(item['name']),
            thumb=plex_util.get_thumb(item['thumb'])
        ))

    pagination.append_controls(oc, response, callback=HandleSeries, path=path, title=title, page=page)

    return oc

@route(PREFIX + '/serie')
def HandleSerie(operation=None, **params):
    oc = ObjectContainer(title2=unicode(params['name']))

    media_info = MediaInfo(**params)

    service.queue.handle_bookmark_operation(operation, media_info)

    serie_info = service.get_serie_info(params['id'])

    for index, item in enumerate(serie_info):
        season = index+1
        season_name = item['pltitle']
        episodes = item['playlist']
        rating_key = service.get_episode_url(params['id'], season, 0)

        new_params = {
            'type': 'season',
            'id': params['id'],
            'serieName': params['name'],
            'name': season_name,
            'thumb': params['thumb'],
            'season': season,
            'episodes': json.dumps(episodes)
        }

        oc.add(SeasonObject(
            key=Callback(HandleSeason, **new_params),
            rating_key=rating_key,
            title=plex_util.sanitize(season_name),
            index=int(season),
            thumb=plex_util.get_thumb(params['thumb'])
        ))

    service.queue.append_bookmark_controls(oc, HandleSerie, media_info)

    return oc

@route(PREFIX + '/season', container=bool)
def HandleSeason(operation=None, container=False, **params):
    oc = ObjectContainer(title2=unicode(params['name']))

    media_info = MediaInfo(**params)

    service.queue.handle_bookmark_operation(operation, media_info)

    if not params['episodes']:
        serie_info = service.get_serie_info(params['id'])
        list = serie_info[int(params['season'])-1]['playlist']
    else:
        list = json.loads(params['episodes'])

    for index, episode in enumerate(list):
        episode_name = episode['comment']
        thumb = service.URL + episode['poster']
        url = episode['file']

        new_params = {
            'type': 'episode',
            'id': url,
            'name': episode_name,
            'serieName': params['serieName'],
            'thumb': thumb,
            'season': params['season'],
            'episode': episode,
            'episodeNumber': index+1
        }

        key = Callback(HandleEpisode, container=container, **new_params)

        oc.add(DirectoryObject(
            key=key,
            title=unicode(episode_name),
            thumb=plex_util.get_thumb(thumb)
        ))

    if str(container) == 'False':
        history.push_to_history(Data, media_info)
        service.queue.append_bookmark_controls(oc, HandleSeason, media_info)

    return oc

@route(PREFIX + '/episode')
def HandleEpisode(operation=None, container=False, **params):
    return HandleMovie(operation=operation, container=container, **params)

@route(PREFIX + '/soundtracks')
def HandleSoundtracks(page=1):
    oc = ObjectContainer(title2=unicode(L('Soundtracks')))

    response = service.get_soundtracks(page=page)

    for item in response['movies']:
        new_params = {
            'type': 'soundtrack',
            'id': item['path'],
            'name': item['name'],
            'thumb': item['thumb']
        }

        oc.add(DirectoryObject(
            key=Callback(HandleSoundtrack, **new_params),
            title=plex_util.sanitize(item['name']),
            thumb=plex_util.get_thumb(item['thumb'])
        ))

    pagination.append_controls(oc, response, callback=HandleSoundtracks, page=page)

    return oc

@route(PREFIX + '/soundtrack')
def HandleSoundtrack(operation=None, container=False, **params):
    oc = ObjectContainer(title2=unicode(params['name']))

    media_info = MediaInfo(**params)

    service.queue.handle_bookmark_operation(operation, media_info)

    albums = service.get_albums(params['id'])

    albums_count = len(albums)

    for index, album in enumerate(albums):
        prefix = str(index + 1) + ". " if albums_count > 1 else ""

        album_name = prefix + album['name']
        thumb = album['thumb']
        artist = album['composer']
        tracks = album['tracks']

        new_params = {
            'type': 'tracks',
            'name': album_name,
            'artist': artist,
            'tracks': json.dumps(tracks)
        }

        oc.add(DirectoryObject(
            key=Callback(HandleTracks, **new_params),
            title=plex_util.sanitize(album_name),
            thumb=plex_util.get_thumb(thumb)
        ))

    if str(container) == 'False':
        history.push_to_history(Data, media_info)
        service.queue.append_bookmark_controls(oc, HandleSoundtrack, media_info)

    return oc

@route(PREFIX + '/selections')
def HandleSelections(page=1):
    oc = ObjectContainer(title2=unicode(L('Selections')))

    response = service.get_selections(page=page)

    for item in response['movies']:
        name = item['name']

        if name != "Актёры и актрисы" and name != "Актеры и актрисы":
            new_params = {
                'type': 'selection',
                'id': item['path'],
                'name': name,
                'thumb': item['thumb'],
            }

            oc.add(DirectoryObject(
                key=Callback(HandleSelection, **new_params),
                title=plex_util.sanitize(name),
                thumb=plex_util.get_thumb(item['thumb'])
            ))

    pagination.append_controls(oc, response, callback=HandleSelections, page=page)

    return oc

@route(PREFIX + '/selection')
def HandleSelection(page=1, operation=None, **params):
    oc = ObjectContainer(title2=unicode(params['name']))

    media_info = MediaInfo(**params)

    service.queue.handle_bookmark_operation(operation, media_info)

    response = service.get_selection(params['id'], page=page)

    for item in response['movies']:
        new_params = {
            'type': 'movie',
            'id': item['path'],
            'name': item['name'],
            'thumb': item['thumb'],
        }

        oc.add(DirectoryObject(
            key=Callback(HandleMovie, **new_params),
            title=plex_util.sanitize(item['name']),
            thumb=plex_util.get_thumb(item['thumb'])
        ))

    service.queue.append_bookmark_controls(oc, HandleSelection, media_info)
    pagination.append_controls(oc, response, page=page, callback=HandleSelection, **media_info)

    return oc

@route(PREFIX + '/movie_filters')
def HandleMovieFilters():
    return HandleFilters(title="Movie Filters", mode='film')

@route(PREFIX + '/serie_filters')
def HandleSerieFilters():
    return HandleFilters(title="Serie Filters", mode='serial')

@route(PREFIX + '/filters')
def HandleFilters(title, mode):
    oc = ObjectContainer(title2=unicode(L(title)))

    response = service.get_filters(mode=mode)

    for item in response:
        for name, list in item.iteritems():
            oc.add(DirectoryObject(
                key=Callback(HandleFilter, mode=mode, name=name, list=json.dumps(list)), title=plex_util.sanitize(name),
            ))

    return oc

@route(PREFIX + '/filter')
def HandleFilter(mode, name, list):
    oc = ObjectContainer(title2=unicode(name))

    if mode == 'film':
        handler = HandleMovies
    else:
        handler = HandleSeries

    for item in json.loads(list):
        name = item['name']
        path = item['path']

        oc.add(DirectoryObject(
            key=Callback(handler, path=path, title=name),
            title=plex_util.sanitize(name),
        ))

    return oc

@route(PREFIX + '/tracks')
def HandleTracks(**params):
    oc = ObjectContainer(title2=unicode(params['name']))

    for track in json.loads(params['tracks']):
        url = track['url']
        name = track['name']
        format = "mp3"
        bitrate = track['bitrate']
        duration = track['duration']

        new_params = MediaInfo(
            type='track',
            id=url,
            name=name,
            artist=params['artist'],
            format=format,
            bitrate=bitrate,
            duration=duration
        )

        oc.add(HandleTrack(**new_params))

    return oc

def build_audio_urls_with_metadata(media_info):
    if 'm4a' in media_info['format']:
        format = 'm4a'
    else:
        format = 'mp3'

    config = FlowBuilder.get_plex_config(format)

    config["bitrate"] = media_info['bitrate']
    config["duration"] = media_info['duration']

    url = media_info['id']

    urls_with_metadata = OrderedDict()

    urls_with_metadata[url] = config

    return urls_with_metadata

@route(PREFIX + '/track')
def HandleTrack(container=False, **params):
    media_info = MediaInfo(**params)

    url_items = build_audio_urls_with_metadata(media_info)

    metadata_object = FlowBuilder.build_metadata_object(media_type=media_info['type'], title=media_info['name'])

    metadata_object.key = Callback(HandleTrack, container=True, **media_info)
    metadata_object.rating_key = unicode(media_info['name'])
    metadata_object.title = unicode(media_info['name'])
    metadata_object.duration = int(media_info['duration'])

    if 'thumb' in media_info:
        metadata_object.artist = media_info['thumb']

    if 'artist' in media_info:
        metadata_object.artist = media_info['artist']

    metadata_object.items.extend(common_routes.MediaObjectsForURL(url_items, common_routes.PlayAudio))

    if container:
        oc = ObjectContainer(title2=unicode(params['name']))

        oc.add(metadata_object)

        return oc
    else:
        return metadata_object

@route(PREFIX + '/search')
def HandleSearch(query=None, page=1):
    oc = ObjectContainer(title2=unicode(L('Search')))

    response = service.search(query=query, page=page)

    for movie in response['movies']:
        name = movie['name']
        thumb = movie['thumb']

        new_params = {
            'id': movie['path'],
            'title': name,
            'name': name,
            'thumb': thumb
        }
        oc.add(DirectoryObject(
            key=Callback(HandleMovieOrSerie, **new_params),
            title=unicode(name),
            thumb=plex_util.get_thumb(thumb)
        ))

    pagination.append_controls(oc, response, callback=HandleSearch, query=query, page=page)

    return oc

@route(PREFIX + '/movie_or_serie')
def HandleMovieOrSerie(**params):
    serie_info = service.get_serie_info(params['id'])

    if serie_info:
        params['type'] = 'serie'
    else:
        params['type'] = 'movie'

    return HandleContainer(**params)

@route(PREFIX + '/container')
def HandleContainer(**params):
    type = params['type']

    if type == 'movie':
        return HandleMovie(**params)
    elif type == 'episode':
        return HandleEpisode(**params)
    elif type == 'season':
        return HandleSeason(**params)
    elif type == 'serie':
        return HandleSerie(**params)
    elif type == 'soundtrack':
        return HandleSoundtrack(**params)
    elif type == 'tracks':
        return HandleTracks(**params)
    elif type == 'selection':
        return HandleSelection(**params)

@route(PREFIX + '/queue')
def HandleQueue():
    oc = ObjectContainer(title2=unicode(L('Queue')))

    service.queue.handle_queue_items(oc, HandleContainer, service.queue.data)

    if len(service.queue.data) > 0:
        oc.add(DirectoryObject(
            key=Callback(ClearQueue),
            title=unicode(L("Clear Queue"))
        ))

    return oc

@route(PREFIX + '/clear_queue')
def ClearQueue():
    service.queue.clear()

    return HandleQueue()

@route(PREFIX + '/history')
def HandleHistory():
    history_object = history.load_history(Data)

    oc = ObjectContainer(title2=unicode(L('History')))

    if history_object:
        data = sorted(history_object.values(), key=lambda k: k['time'], reverse=True)

        service.queue.handle_queue_items(oc, HandleContainer, data)

    return oc
