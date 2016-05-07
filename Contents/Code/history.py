KEY_HISTORY = 'history'
HISTORY_SIZE = 60

def push_to_history(item):
    history = Data.LoadObject(KEY_HISTORY)

    if not history:
        history = {}

    path = item['path']

    history[path] = {
        'type': item['type'],
        'path': item['path'],
        'name': item['name'],
        'thumb': item['thumb'],
        'time': Datetime.TimestampFromDatetime(Datetime.Now())
    }

    if 'season' in item:
        history[path]['season'] = item['season']

    if 'episode' in item:
        history[path]['episode'] = item['episode']

    # Trim old items
    if len(history) > HISTORY_SIZE:
        items = sorted(
            history.values(),
            key=lambda k: k['time'],
            reverse=True
        )[:HISTORY_SIZE]

        history = {}

        for it in items:
            history[it['path']] = it

    Data.SaveObject(KEY_HISTORY, history)

def load_history():
    return Data.LoadObject(KEY_HISTORY)