from services import api
from store.toolkit import create_async_thunk

handle_action_login = create_async_thunk('auth/login', lambda payload: api.post('/login', payload))

handle_action_register = create_async_thunk('auth/register', lambda payload: api.post('/register', payload))

get_profile = create_async_thunk('auth/profile', lambda _payload: api.get('/check-auth'))
