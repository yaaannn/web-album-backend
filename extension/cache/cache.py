import logging
import pickle
from functools import wraps
from typing import Any, Callable

import redis
from django.conf import settings
from rest_framework.response import Response


class CacheDecorator:
    def __init__(self, cache_type: str, cache_timeout: int = 300) -> None:
        self._cache_type = cache_type
        self._redis = redis.Redis(
            connection_pool=redis.ConnectionPool().from_url(
                settings.CACHES["api"]["LOCATION"]
            )
        )
        self._cache_timeout = cache_timeout

    def __call__(self, func: Callable) -> Callable:
        @wraps(func)
        def wrapper(re_self, request, *args: Any, **kwds: Any) -> Any:
            try:
                # 如果涉及到写数据库，执行原方法，并且清空缓存
                if self._cache_type == "w":
                    res = func(re_self, request, *args, **kwds)
                    # 清除所有缓存
                    self._redis.flushdb(1)
                    return res
                # 获取请求路径和参数
                payload = f"{request.path}+{request.GET}"
                # mutex = threading.Lock()
                # locked = mutex.acquire(timeout=20)
                # 如果加锁成功，就先查缓存
                cache_val = self._redis.get(payload)
                # 如果缓存未命中，获取响应并且添加缓存
                if not cache_val:
                    logging.debug("缓存未命中")
                    response = func(re_self, request, *args, **kwds)
                    if response.status_code == 200:
                        if hasattr(response, "_headers"):
                            headers = response._headers.copy()
                        else:
                            headers = {k: (k, v) for k, v in response.items()}
                        response_triple = (response.data, response.status_code, headers)
                        self._redis.setex(
                            payload,
                            self._cache_timeout,
                            pickle.dumps(response_triple),
                        )
                    # mutex.release()
                    return response
                logging.debug("缓存命中")
                content, status, headers = pickle.loads(cache_val)
                # mutex.release()
                return Response(data=content, status=status, headers=headers)
            except Exception as e:
                logging.exception(e)

        return wrapper
