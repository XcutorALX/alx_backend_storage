#!/usr/bin/env python3
"""
Contains a cache class
"""

import redis
import uuid
from typing import Union, Callable
from functools import wraps


def count_calls(method: Callable) -> Callable:
    """count calls function
    this function increments a key of the function name
    using redis everytime the function is called
    """

    key = method.__qualname__

    @wraps(method)
    def wrapper(self, *args, **kwargs) -> str:
        """wrapper function
        """
        self._redis.incr(key)
        return method(self, *args, **kwargs)

    return wrapper


def call_history(method: Callable) -> Callable:
    """stores the history of inputs and outputs for a particular function
    """
    @wraps(method)
    def wrapper(self, *args, **kwargs):
        """saves the input and output of each function in redis
        """
        input_key = method.__qualname__ + ":inputs"
        output_key = method.__qualname__ + ":outputs"

        output = method(self, *args, **kwargs)

        self._redis.rpush(input_key, str(args))
        self._redis.rpush(output_key, str(output))

        return output

    return wrapper


class Cache:
    """Cache class
    """

    def __init__(self):
        """Init method"""
        self._redis = redis.Redis()

        self._redis.flushdb()

    @count_calls
    def store(self, data: Union[str, bytes, int, float]) -> str:
        """store method"""
        key = str(uuid.uuid1())

        self._redis.set(key, data)

        return (key)

    def get(self, key: str, fn: Callable = None):
        """get method"""
        data = self._redis.get(key)

        if fn and data is not None:
            data = fn(data)

        return data

    def get_str(self, key: str) -> str:
        """get str method"""
        data = self._redis.get(key)

        return data.decode('UTF-8')

    def get_int(self, key: str) -> int:
        """get int method"""
        data = self._redis.get(key)

        try:
            data = int(data.decode('UTF-8'))
        except Exception:
            data = 0

        return data
