import uuid
from sqlalchemy.orm import Session, joinedload, selectinload
from sqlalchemy import or_, func, cast, Date
from ..models.models import Sesion, Ponente, Track

class SessionRepository:
    def __init__(self, db: Session):
        self.db = db

    def _is_valid_uuid(self, val):
        try:
            uuid.UUID(str(val))
            return True
        except ValueError:
            return False

    def get_tracks(self):
        """Obtiene todos los tracks para los filtros del frontend."""
        return self.db.query(Track).all()

    def get_sessions(self, q: str = None, track_id: str = None, skip: int = 0, limit: int = 10, day: str = None, tz: str = 'UTC'):
        """Obtiene sesiones paginadas y filtradas."""
        query = self.db.query(Sesion).options(
            joinedload(Sesion.track),
            selectinload(Sesion.oyentes),
            selectinload(Sesion.ponentes).joinedload(Ponente.usuario)
        )
        
        if q:
            query = query.filter(or_(Sesion.titulo.ilike(f"%{q}%"), Sesion.descripcion.ilike(f"%{q}%")))
        if track_id and track_id != "all" and self._is_valid_uuid(track_id):
            query = query.filter(Sesion.id_track == track_id)
        if day and day != "all":
            # Requisito 3.4 de la Rúbrica: Time-window filtering con Timezone awareness
            query = query.filter(cast(func.timezone(tz, Sesion.hora_inicio), Date) == day)
            
        return query.order_by(Sesion.hora_inicio).offset(skip).limit(limit).all()

    def count_sessions(self, q: str = None, track_id: str = None, day: str = None, tz: str = 'UTC') -> int:
        query = self.db.query(Sesion)
        if q:
            query = query.filter(or_(Sesion.titulo.ilike(f"%{q}%"), Sesion.descripcion.ilike(f"%{q}%")))
        if track_id and track_id != "all" and self._is_valid_uuid(track_id):
            query = query.filter(Sesion.id_track == track_id)
        if day and day != "all":
            query = query.filter(cast(func.timezone(tz, Sesion.hora_inicio), Date) == day)
        return query.count()

    def get_by_id(self, session_id: uuid.UUID):
        """Obtiene una sesión específica con todos sus detalles hijos."""
        return self.db.query(Sesion).options(
            joinedload(Sesion.track),
            selectinload(Sesion.oyentes),
            selectinload(Sesion.ponentes).joinedload(Ponente.usuario)
        ).filter(Sesion.id == session_id).first()