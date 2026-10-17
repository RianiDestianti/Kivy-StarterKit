import os
from kivy.storage.jsonstore import JsonStore

TOKEN_KEY = "auth-key"

_store = None


def _get_store():
    global _store
    if _store is None:
        from kivy.app import App
        app = App.get_running_app()
        directory = app.user_data_dir if app else os.getcwd()
        _store = JsonStore(os.path.join(directory, 'session.json'))
    return _store


def get_token():
    store = _get_store()
    return store.get(TOKEN_KEY)['value'] if store.exists(TOKEN_KEY) else None


def set_token(token):
    _get_store().put(TOKEN_KEY, value=token)


def remove_token():
    store = _get_store()
    if store.exists(TOKEN_KEY):
        store.delete(TOKEN_KEY)
