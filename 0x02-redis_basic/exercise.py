#!/usr/bin/env python3
"""
Redis caching implementation
"""
import redis
import uuid
from typing import Union, Callable, Optional
from functools import wraps


def call_history(method: Callable) -> Callable:
    """
    Stores input params passed to a method and
    output values returned by the method.
    """
    inputs = method.__qualname__ + ':inputs'
    outputs = method.__qualname__ + ':outputs'

    @wraps(method)
    def wrapper(self, *args, **kwargs):
        self._redis.rpush(inputs, str(args))
        result = method(self, *args, **kwargs)
        self._redis.rpush(outputs, str(result))
        return result
    return wrapper


def count_calls(method: Callable) -> Callable:
    """ Returns a function that increments the number of calls
        the passed method has. also returning the return value of
        the passed method.
    """
    key = method.__qualname__

    @wraps(method)
    def wrapper(self, *args, **kwargs):
        self._redis.incr(key)
        return method(self, *args, **kwargs)
    return wrapper


def replay(method: Callable) -> str:
    """ retrieves cached information from the database """
    name = method.__qualname__
    redis_inst = method.__self__._redis
    _class = method.__self__
    call_Count = redis_inst.get(name)
    args = redis_inst.lrange(name + ':inputs', 0, -1)
    results = redis_inst.lrange(name + ':outputs', 0, -1)
    print('{} was called {} times:'.format(name, int(call_Count)))
    pack = zip(args, results)

    for items in pack:
        print('{}(*{}) -> {}'.format(name,
                                     _class.get_str(items[0]),
                                     _class.get_str(items[1])))


class Cache:
    """ Cache implementation with redis """
    def __init__(self):
        """ Init method """
        self._redis = redis.Redis()
        self._redis.flushdb()

    @count_calls
    @call_history
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
