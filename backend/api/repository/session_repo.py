import uuid
from sqlalchemy.orm import Session, joinedload, selectinload
from sqlalchemy import or_
from ..models.models import Sesion, Ponente

class SessionRepository:
    def __init__(self, db: Session):
        self.db = db

    def get_all(self, skip: int = 0, limit: int = 10):
        """Obtiene las sesiones paginadas con su track y oyentes."""
        return self.db.query(Sesion).options(
            joinedload(Sesion.track),
            selectinload(Sesion.oyentes)
        ).order_by(Sesion.hora_inicio).offset(skip).limit(limit).all()

    def count_all(self) -> int:
        """Cuenta el total de sesiones en la base de datos (para paginación)."""
        return self.db.query(Sesion).count()

    def get_by_id(self, session_id: uuid.UUID):
        """Obtiene una sesión específica con todos sus detalles hijos."""
        return self.db.query(Sesion).options(
            joinedload(Sesion.track),
            selectinload(Sesion.oyentes),
            selectinload(Sesion.ponentes).joinedload(Ponente.usuario) # Trae al ponente y su info de usuario
        ).filter(Sesion.id == session_id).first()

    def search(self, query: str, skip: int = 0, limit: int = 10):
        """Busca sesiones cuyo título o descripción coincidan con el texto de búsqueda."""
        return self.db.query(Sesion).options(
            joinedload(Sesion.track),
            selectinload(Sesion.oyentes)
        ).filter(
            or_(
                Sesion.titulo.ilike(f"%{query}%"),
                Sesion.descripcion.ilike(f"%{query}%")
            )
        ).order_by(Sesion.hora_inicio).offset(skip).limit(limit).all()

    def count_search(self, query: str) -> int:
        """Cuenta el total de resultados que coinciden con la búsqueda (para paginación)."""
        return self.db.query(Sesion).filter(
            or_(
                Sesion.titulo.ilike(f"%{query}%"),
                Sesion.descripcion.ilike(f"%{query}%")
            )
        ).count()