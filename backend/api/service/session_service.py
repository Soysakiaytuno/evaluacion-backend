import uuid
from .session_data_service import SessionDataService
from .cache_service import CacheService

class SessionService:
    """Main Service que orquesta la caché y la obtención de datos."""
    def __init__(self, data_service: SessionDataService, cache_service: CacheService):
        self.data_service = data_service
        self.cache_service = cache_service

    def get_tracks(self) -> list:
        cache_key = "tracks:all"
        
        cached = self.cache_service.get(cache_key)
        if cached:
            return cached

        response = self.data_service.get_tracks_formatted()
        self.cache_service.set(cache_key, response)
        return response

    def get_sessions(self, page: int, page_size: int, q: str = None, track: str = None, day: str = None, tz: str = None) -> dict:
        tz_safe = tz if tz else 'UTC'
        cache_key = f"sessions:{page}:{page_size}:{q}:{track}:{day}:{tz_safe}"
        
        cached = self.cache_service.get(cache_key)
        if cached:
            return cached

        response = self.data_service.get_sessions_formatted(page=page, page_size=page_size, q=q, track=track, day=day, tz=tz_safe)
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
    def get_agenda(self, oyente_id: uuid.UUID):
        response = self.data_service.get_agenda(oyente_id)
        return response