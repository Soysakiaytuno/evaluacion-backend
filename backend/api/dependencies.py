from fastapi import Depends
from sqlalchemy.orm import Session
from redis import Redis

from .database import get_db
from .redis import get_redis
from .repository.session_repo import SessionRepository
from .service.session_service import SessionService
from .service.session_data_service import SessionDataService
from .service.cache_service import CacheService

def get_session_repository(db: Session = Depends(get_db)) -> SessionRepository:
    return SessionRepository(db=db)

def get_cache_service(cache: Redis = Depends(get_redis)) -> CacheService:
    return CacheService(cache=cache)

def get_session_data_service(repo: SessionRepository = Depends(get_session_repository)) -> SessionDataService:
    return SessionDataService(repository=repo)

def get_session_service(
    data_service: SessionDataService = Depends(get_session_data_service),
    cache_service: CacheService = Depends(get_cache_service)
) -> SessionService:
    return SessionService(data_service=data_service, cache_service=cache_service)