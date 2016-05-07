import main
import util
from media_info import MediaInfo

@route(constants.PREFIX + '/queue')
def HandleQueue():
    oc = ObjectContainer(title2=unicode(L('Queue')))

    for media_info in service.queue.data:
        if media_info.type == MediaInfo.EPISODE:
            oc.add(DirectoryObject(
                key=Callback(main.HandleMovie, type=media_info.type, **media_info),
                title=util.sanitize(media_info['name']),
                thumb=media_info['thumb']
            ))

        elif media_info.type == MediaInfo.SEASON:
            oc.add(DirectoryObject(
                key=Callback(main.HandleSeasons, type=media_info.type, **media_info),
                title=util.sanitize(media_info['name']),
                thumb=media_info['thumb']
            ))

        elif media_info.type == MediaInfo.VIDEO:
            oc.add(DirectoryObject(
                key=Callback(main.HandleMovie, type=media_info.type, **media_info),
                title=util.sanitize(media_info['name']),
                thumb=media_info['thumb']
            ))

        elif media_info.type == MediaInfo.AUDIO:
            oc.add(DirectoryObject(
                key=Callback(main.HandleSoundtrack, type=media_info.type, **media_info),
                title=util.sanitize(media_info['name']),
                thumb=media_info['thumb']
            ))

        else:
            oc.add(DirectoryObject(
                key=Callback(main.HandleContainer, type=media_info.type, **media_info),
                title=util.sanitize(media_info['name']),
                thumb=media_info['thumb']
            ))

    return oc
