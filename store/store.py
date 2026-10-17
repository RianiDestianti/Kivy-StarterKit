from store.toolkit import configure_store
from store.slices.auth_slice import auth_slice
from store.slices.user_slice import user_slice

store = configure_store({
    'auth'      : auth_slice.reducer,
    'user'      : user_slice.reducer,
})
