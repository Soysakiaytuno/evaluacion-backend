import json
import logging
from redis import Redis
from redis.exceptions import RedisError

logger = logging.getLogger(__name__)

class CacheService:
    """Servicio dedicado exclusivamente a gestionar Redis y la degradación elegante."""
    def __init__(self, cache: Redis, ttl: int = 300):
        self.cache = cache
        self.ttl = ttl

    def get(self, key: str):
        try:
            data = self.cache.get(key)
            if data:
                return json.loads(data)
        except RedisError as e:
            logger.warning(f"Error al leer de Redis (Degradación elegante): {e}")
        return None

    def set(self, key: str, data: dict):
        try:
            self.cache.setex(key, self.ttl, json.dumps(data))
        except RedisError as e:
            logger.warning(f"Error al escribir en Redis (Degradación elegante): {e}")