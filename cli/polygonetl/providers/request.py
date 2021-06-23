import logging

import lru
import requests
from requests.adapters import HTTPAdapter

from web3.utils.caching import (
    generate_cache_key,
)


def _remove_session(key, session):
    session.close()


_session_cache = lru.LRU(8, callback=_remove_session)


MAX_POOL_SIZE = 40


def _get_session(*args, **kwargs):
    cache_key = generate_cache_key((args, kwargs))
    if cache_key not in _session_cache:
        session = requests.Session()
        session.mount('https://', HTTPAdapter(pool_maxsize=MAX_POOL_SIZE))
        session.mount('http://', HTTPAdapter(pool_maxsize=MAX_POOL_SIZE))
        _session_cache[cache_key] = session
    return _session_cache[cache_key]


def make_post_request(endpoint_uri, data, *args, **kwargs):
    kwargs.setdefault('timeout', 10)
    session = _get_session(endpoint_uri)
    response = session.post(endpoint_uri, data=data, *args, **kwargs)
    try:
        response.raise_for_status()
    except Exception as e:
        logging.error('Exception occurred while making a post request, response body was: ' + (response.text or ''))
        raise e

    return response.content
