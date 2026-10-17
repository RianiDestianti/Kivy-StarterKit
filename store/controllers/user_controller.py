from urllib.parse import quote
from services import api
from store.toolkit import create_async_thunk


def _get_list_user(query):
    keyword = quote(query.get('keyword', ''))
    page    = query.get('page', 1)
    limit   = query.get('limit', 10)
    return api.get(f"/admin/users?keyword={keyword}&page={page}&limit={limit}")


get_list_user = create_async_thunk('user/getList', _get_list_user)

save_user = create_async_thunk('user/saveUser', lambda payload: api.post('/admin/user/action', payload))

delete_user = create_async_thunk('user/deleteUser', lambda user_id: api.get(f"/admin/user/delete/{user_id}"))
