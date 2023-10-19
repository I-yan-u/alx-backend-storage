#!/usr/bin/env python3
"""
Implements an expiring web cache and tracker
"""
from typing import Callable
from functools import wraps
import redis
import requests
# import time
redis_client = redis.Redis()


def url_count(method: Callable) -> Callable:
    """counts how many times an url is accessed"""
    @wraps(method)
    def wrapper(*args, **kwargs):
        url = args[0]
        redis_client.incr(f"count:{url}")
        cached = redis_client.get(f'{url}')
        if cached:
            # print('Cached: \n{}'.format(cached.decode('utf-8')))
            return cached.decode('utf-8')
        res = method(url)
        redis_client.setex(url, 10, res)
        # print(res)
        return method(*args, **kwargs)
    return wrapper


@url_count
def get_page(url: str) -> str:
    """get a page and cache value"""
    response = requests.get(url)
    return response.text


if __name__ == "__main__":
    # start = time.perf_counter()
    get_page('http://slowwly.robertomurray.co.uk')
    # print(time.perf_counter() - start)
