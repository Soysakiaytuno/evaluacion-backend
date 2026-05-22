import os
import redis

REDIS_URL = os.getenv("REDIS_URL", "redis://cache:6379/0")

class Redis:
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(Redis, cls).__new__(cls)
            cls._instance.client = redis.from_url(REDIS_URL, decode_responses=True)
        return cls._instance

    def get_client(self):
        return self.client

redis_singleton = Redis()

def get_redis():
    return redis_singleton.get_client()