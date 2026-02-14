import redis
from flask import current_app


def get_redis_client():
    return redis.Redis(
        host="localhost",
        port=6379,
        decode_responses=True
    )