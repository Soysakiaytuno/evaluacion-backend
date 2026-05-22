import uuid
from .session_data_service import SessionDataService
from .cache_service import CacheService

class SessionService:
    """Main Service que orquesta la caché y la obtención de datos."""
    def __init__(self, data_service: SessionDataService, cache_service: CacheService):
        self.data_service = data_service
        self.cache_service = cache_service

    def get_all(self, skip: int = 0, limit: int = 10) -> dict:
        cache_key = f"sessions:all:{skip}:{limit}"
        
        cached = self.cache_service.get(cache_key)
        if cached:
            return cached

        response = self.data_service.get_all_formatted(skip=skip, limit=limit)
        self.cache_service.set(cache_key, response)
        return response

    def get_by_id(self, session_id: uuid.UUID) -> dict | None:
        cache_key = f"sessions:detail:{session_id}"
        
        cached = self.cache_service.get(cache_key)
        if cached:
            return cached

        response = self.data_service.get_by_id_formatted(session_id)
        if response:
            self.cache_service.set(cache_key, response)
        return response

    def search(self, query: str, skip: int = 0, limit: int = 10) -> dict:
        cache_key = f"sessions:search:{query}:{skip}:{limit}"
        
        cached = self.cache_service.get(cache_key)
        if cached:
            return cached

        response = self.data_service.search_formatted(query=query, skip=skip, limit=limit)
        self.cache_service.set(cache_key, response)
        return response