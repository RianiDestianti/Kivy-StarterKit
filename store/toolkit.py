"""
Redux Toolkit versi kecil untuk Kivy.

    create_async_thunk  -> seperti createAsyncThunk (pending / fulfilled / rejected)
    create_slice        -> seperti createSlice (reducers + extra_reducers)
    Store               -> seperti configureStore (dispatch, get_state, select)

Thunk dijalankan di background thread supaya UI tidak macet, lalu hasilnya
di-dispatch kembali di main thread lewat Clock (aturan Kivy: UI hanya boleh diubah dari main thread).
"""
import copy
import threading
from kivy.clock import Clock
from kivy.event import EventDispatcher
from kivy.properties import DictProperty


class AsyncThunk:
    def __init__(self, type_prefix, payload_creator):
        self.type_prefix = type_prefix
        self.payload_creator = payload_creator
        self.pending = f"{type_prefix}/pending"
        self.fulfilled = f"{type_prefix}/fulfilled"
        self.rejected = f"{type_prefix}/rejected"

    def __call__(self, argument=None):
        def thunk(dispatch, get_state):
            dispatch({ 'type': self.pending, 'meta': { 'arg': argument } })

            def worker():
                try:
                    payload = self.payload_creator(argument)
                    action = { 'type': self.fulfilled, 'payload': payload, 'meta': { 'arg': argument } }
                except Exception as error:
                    action = { 'type': self.rejected, 'error': { 'message': str(error) }, 'meta': { 'arg': argument } }

                Clock.schedule_once(lambda _elapsed: dispatch(action))

            threading.Thread(target=worker, daemon=True).start()

        return thunk


def create_async_thunk(type_prefix, payload_creator):
    return AsyncThunk(type_prefix, payload_creator)


class Slice:
    def __init__(self, name, initial_state, reducers, extra_reducers):
        self.name = name
        self.initial_state = initial_state
        self.case_reducers = {}
        self.actions = {}

        for reducer_name, handler in reducers.items():
            action_type = f"{name}/{reducer_name}"
            self.case_reducers[action_type] = handler
            self.actions[reducer_name] = self._action_creator(action_type)

        self.case_reducers.update(extra_reducers)

    @staticmethod
    def _action_creator(action_type):
        return lambda payload=None: { 'type': action_type, 'payload': payload }

    def reducer(self, state, action):
        if state is None:
            state = copy.deepcopy(self.initial_state)

        handler = self.case_reducers.get(action['type'])
        if not handler:
            return state

        # Seperti immer di Redux Toolkit: reducer boleh langsung mengubah state (yang sudah disalin).
        draft = copy.deepcopy(state)
        handler(draft, action)
        return draft


def create_slice(name, initial_state, reducers=None, extra_reducers=None):
    return Slice(name, initial_state, reducers or {}, extra_reducers or {})


class Store(EventDispatcher):
    state = DictProperty({})

    def __init__(self, reducers, **kwargs):
        super().__init__(**kwargs)
        self.reducers = reducers
        self.state = { name: reducer(None, { 'type': '@@INIT' }) for name, reducer in reducers.items() }

    def get_state(self):
        return self.state

    def dispatch(self, action):
        if callable(action):
            return action(self.dispatch, self.get_state)

        self.state = { name: reducer(self.state.get(name), action) for name, reducer in self.reducers.items() }
        return action

    def select(self, selector, callback):
        """Seperti useAppSelector: callback dipanggil sekarang dan setiap kali hasil selector berubah."""
        last_value = { 'value': selector(self.state) }
        callback(last_value['value'])

        def on_change(_store, state):
            value = selector(state)
            if value != last_value['value']:
                last_value['value'] = value
                callback(value)

        self.bind(state=on_change)
        return lambda: self.unbind(state=on_change)


def configure_store(reducers):
    return Store(reducers)
