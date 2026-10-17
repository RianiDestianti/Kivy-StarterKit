from typing import Optional, TypedDict


class ResponseLoginType(TypedDict):
    key         : str
    email       : str


class LoginRequest(TypedDict, total=False):
    email       : str
    password    : str


class RegisterRequest(TypedDict):
    name        : str
    email       : str
    password    : str


class DataAuthType(TypedDict):
    id          : int
    name        : str
    email       : str
    role        : str
    avatar      : Optional[str]
    verified    : bool


class AuthState(TypedDict):
    loading             : bool
    response_login      : Optional[ResponseLoginType]
    response_register   : Optional[ResponseLoginType]
    error               : Optional[str]
    error_fields        : Optional[dict]
    error_code          : Optional[int]
    profile             : Optional[DataAuthType]
