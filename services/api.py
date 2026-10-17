import os
import requests
from libs.storage import get_token

TIMEOUT = 10


def _headers():
    headers = { 'Content-Type': 'application/json' }
    token = get_token()
    if token:
        headers['Authorization'] = f"Bearer {token}"
    return headers


def _parse(response):
    # Backend mengembalikan { status, message, data } juga untuk 401/403/404,
    # jadi response error tetap diteruskan ke slice seperti response biasa.
    body = response.json()
    if isinstance(body, dict) and body.get('status'):
        return body
    response.raise_for_status()
    return body


def get(path):
    return _parse(requests.get(os.getenv('API_URL', '') + path, headers=_headers(), timeout=TIMEOUT))


def post(path, payload):
    return _parse(requests.post(os.getenv('API_URL', '') + path, json=payload, headers=_headers(), timeout=TIMEOUT))
