#!/usr/bin/env python3
"""
Redis caching implementation
"""
import redis
import uuid
from typing import Union, Callable, Optional

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

    def get(self, key: str, fn: Optional[Callable] = None) -> str:
        """ Get data from cached storage """
        data = self._redis.get(key)
        if fn:
            return fn(data)
        return data

    def get_str(self, data: str) -> str:
        """ returns string form of data """
        return data.decode('utf-8')
    
    def get_int(self, data: str) -> int:
        """ returns integer form of data """
        return int(data)
