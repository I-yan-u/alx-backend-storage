#!/usr/bin/env python3
"""
Redis caching implementation
"""
import redis
import uuid
from typing import Union

class Cache:
    """ Cache implementation with redis """
    def __init__(self):
        """ Init method """
        self._redis = redis.Redis()
        self._redis.flushdb()

    def store(self, data: Union[str, int, float, bytes]) -> str:
        """ cache storage method """
        key = str(uuid.uuid4())
        self._redis.mset({key: data})
        return key
