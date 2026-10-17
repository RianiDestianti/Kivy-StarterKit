from store.toolkit import create_slice
from store.controllers.auth_controller import get_profile, handle_action_login, handle_action_register

initial_state = {
    'loading'           : False,
    'response_login'    : None,
    'response_register' : None,
    'error'             : None,
    'error_fields'      : None,
    'error_code'        : None,
    'profile'           : None,
}


def handle_clean_response(state, action):
    state['response_login']     = None
    state['response_register']  = None
    state['error']              = None
    state['error_fields']       = None


def handle_logout(state, action):
    state['profile']            = None
    state['error_code']         = None


def _pending(state, action):
    state['loading']            = True
    state['error']              = None
    state['error_fields']       = None


def _rejected(state, action):
    state['loading']            = False
    state['error']              = action['error']['message'] or 'Network error'


def _login_fulfilled(state, action):
    state['loading']            = False
    response                    = action['payload']

    if response['status'] == 200:
        state['response_login'] = response['data']
        state['error']          = None
    else:
        state['error']          = response['message']
        state['error_fields']   = response.get('data') if response['status'] == 422 else None


def _register_fulfilled(state, action):
    state['loading']            = False
    response                    = action['payload']

    if response['status'] == 200:
        state['response_register'] = response['data']
        state['error']             = None
    else:
        state['error']          = response['message']
        state['error_fields']   = response.get('data') if response['status'] == 422 else None


def _profile_pending(state, action):
    state['loading']            = True


def _profile_fulfilled(state, action):
    state['loading']            = False
    state['error_code']         = action['payload']['status']
    state['profile']            = action['payload'].get('data') if action['payload']['status'] == 200 else None


auth_slice = create_slice(
    name            = 'auth',
    initial_state   = initial_state,
    reducers        = {
        'handle_clean_response' : handle_clean_response,
        'handle_logout'         : handle_logout,
    },
    extra_reducers  = {
        handle_action_login.pending         : _pending,
        handle_action_login.fulfilled       : _login_fulfilled,
        handle_action_login.rejected        : _rejected,

        handle_action_register.pending      : _pending,
        handle_action_register.fulfilled    : _register_fulfilled,
        handle_action_register.rejected     : _rejected,

        get_profile.pending                 : _profile_pending,
        get_profile.fulfilled               : _profile_fulfilled,
        get_profile.rejected                : _rejected,
    }
)

actions = auth_slice.actions
