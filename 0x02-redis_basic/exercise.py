#!/usr/bin/env python3
"""
Contains a cache class
"""

import redis
import uuid
from typing import Union
from functools import wraps


def count_calls(method: callable) -> callable:
    """count calls function
    this function increments a key of the function name
    using redis everytime the function is called
    """

    key = method.__qualname__

    @wraps(method)
    def wrapper(self, *args, **kwargs):
        """wrapper function
        """
        self._redis.incr(key)
        return method(self, *args, **kwargs)

    return wrapper


class Cache:
    """Cache class
    """

    def __init__(self):
        self._redis = redis.Redis()

        self._redis.flushdb()

    @count_calls
    def store(self, data: Union[str, bytes, int, float]) -> str:
        key = str(uuid.uuid1())

        self._redis.set(key, data)

        return (key)

    def get(self, key: str, fn: callable = None):

        data = self._redis.get(key)

        if fn and data is not None:
            data = fn(data)

        return data

    def get_str(self, key: str) -> str:
        data = self._redis.get(key)

        return data.decode('UTF-8')

    def get_int(self, key: str) -> int:
        data = self._redis.get(key)

        try:
            data = int(data.decode('UTF-8'))
        except Exception:
            data = 0

        return data
