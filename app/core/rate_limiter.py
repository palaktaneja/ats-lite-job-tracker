import time
from app.core.redis_client import get_redis_client
from app.core.exceptions import ForbiddenException


def rate_limit(key: str, limit: int, window_seconds: int):
    redis_client = get_redis_client()

    current = redis_client.get(key)

    if current and int(current) >= limit:
        raise ForbiddenException("Rate limit exceeded. Try again later.")

    pipe = redis_client.pipeline()
    pipe.incr(key, 1)
    pipe.expire(key, window_seconds)
    pipe.execute()