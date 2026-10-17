from typing import Optional, TypedDict


class User(TypedDict):
    id          : int
    name        : str
    phone       : Optional[str]
    email       : str
    avatar      : Optional[str]
    role        : str


class UserTotal(TypedDict):
    pages       : int
    data        : int


class UserState(TypedDict):
    users       : list
    page        : int
    total       : UserTotal
    loading     : bool
    response    : dict
    error       : Optional[str]


class UserQuery(TypedDict, total=False):
    page        : int
    limit       : int
    keyword     : str
