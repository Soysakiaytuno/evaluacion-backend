from redis import Redis
from ..repository.session_repo import SessionRepository

class SessionService:
    def __init__(self, repository: SessionRepository, cache: Redis):
        self.repository = repository
        self.cache = cache
    # La lógica de negocio (caché, cálculo de asientos) irá aquí.