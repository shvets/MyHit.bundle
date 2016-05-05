KEY_HISTORY = 'history'
HISTORY_SIZE = 60

def push_to_history(**params):
    history = Data.LoadObject(KEY_HISTORY)

    if not history:
        history = {}

    path = params['path']

    history[path] = {
        'path': params['path'],
        'name': params['name'],
        'thumb': params['thumb'],
        'time': Datetime.TimestampFromDatetime(Datetime.Now())
    }

    if 'season' in params:
        history[path]['season'] = params['season']

    if 'episode' in params:
        history[path]['episode'] = params['episode']

    # Trim old items
    if len(history) > HISTORY_SIZE:
        items = sorted(
            history.values(),
            key=lambda k: k['time'],
            reverse=True
        )[:HISTORY_SIZE]

        history = {}

        for item in items:
            history[item['path']] = item

    Data.SaveObject(KEY_HISTORY, history)

def load_history():
    return Data.LoadObject(KEY_HISTORY)