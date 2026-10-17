from store.toolkit import create_slice
from store.controllers.user_controller import delete_user, get_list_user, save_user

initial_state = {
    'users'         : [],
    'page'          : 1,
    'total'         : {
        'pages'     : 0,
        'data'      : 0,
    },
    'response'      : {
        'action'    : None,
        'delete'    : None,
    },
    'loading'       : False,
    'error'         : None,
}


def reset_response(state, action):
    state['response'] = {
        'action'    : None,
        'delete'    : None,
    }


def _pending(state, action):
    state['loading'] = True


def _rejected(state, action):
    state['loading'] = False
    state['error']   = action['error']['message'] or 'Network error'


def _list_fulfilled(state, action):
    state['loading'] = False
    response         = action['payload']

    if response['status'] == 200:
        state['users']  = response['data']['data']
        state['page']   = response['data']['page']
        state['total']  = response['data']['total']
        state['error']  = None
    else:
        state['error']  = response['message']


def _save_fulfilled(state, action):
    state['loading']            = False
    state['response']['action'] = action['payload']


def _delete_fulfilled(state, action):
    state['loading']            = False
    state['response']['delete'] = action['payload']

    if action['payload']['status'] == 200:
        deleted_id              = action['meta']['arg']
        state['users']          = [item for item in state['users'] if item['id'] != deleted_id]
        state['total']['data']  = max(0, state['total']['data'] - 1)


user_slice = create_slice(
    name            = 'user',
    initial_state   = initial_state,
    reducers        = {
        'reset_response'    : reset_response,
    },
    extra_reducers  = {
        get_list_user.pending   : _pending,
        get_list_user.fulfilled : _list_fulfilled,
        get_list_user.rejected  : _rejected,

        save_user.pending       : _pending,
        save_user.fulfilled     : _save_fulfilled,
        save_user.rejected      : _rejected,

        delete_user.pending     : _pending,
        delete_user.fulfilled   : _delete_fulfilled,
        delete_user.rejected    : _rejected,
    }
)

actions = user_slice.actions
