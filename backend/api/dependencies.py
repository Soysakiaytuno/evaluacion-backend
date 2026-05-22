from fastapi import Depends
from sqlalchemy.orm import Session
from redis import Redis

from .database import get_db
from .redis import get_redis
from .repository.session_repo import SessionRepository
from .service.session_service import SessionService

def get_session_repository(db: Session = Depends(get_db)) -> SessionRepository:
    return SessionRepository(db=db)

def get_session_service(
    repo: SessionRepository = Depends(get_session_repository),
    cache: Redis = Depends(get_redis)
) -> SessionService:
    return SessionService(repository=repo, cache=cache)