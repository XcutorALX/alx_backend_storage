#!/usr/bin/env python3
"""
Contains a cache class
"""

import redis
import uuid
from typing import Union


class Cache:
    """Cache class
    """

    def __init__(self):
        self._redis = redis.Redis()

        self._redis.flushdb()

    def store(self, data: Union[str, bytes, int, float]) -> str:
        key = str(uuid.uuid1())

        self._redis.set(key, data)

        return (key)
