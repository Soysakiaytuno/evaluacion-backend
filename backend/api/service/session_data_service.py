import uuid
from ..repository.session_repo import SessionRepository
from ..schemas import SesionListadoSchema, SesionDetalleSchema

class SessionDataService:
    """Servicio encargado de la lógica de negocio y transformación de datos."""
    def __init__(self, repository: SessionRepository):
        self.repository = repository

    def _calculate_available_seats(self, session) -> int:
        """Calcula la disponibilidad restando los oyentes a la capacidad total."""
        return max(0, session.capacidad - len(session.oyentes))

    def get_all_formatted(self, skip: int, limit: int) -> dict:
        db_sessions = self.repository.get_all(skip=skip, limit=limit)
        total = self.repository.count_all()

        items = []
        for session in db_sessions:
            session.asientos_disponibles = self._calculate_available_seats(session)
            items.append(SesionListadoSchema.model_validate(session).model_dump(mode="json"))

        return {
            "total": total,
            "page": (skip // limit) + 1 if limit > 0 else 1,
            "size": limit,
            "pages": (total + limit - 1) // limit if limit > 0 else 1,
            "items": items
        }

    def get_by_id_formatted(self, session_id: uuid.UUID) -> dict | None:
        session = self.repository.get_by_id(session_id)
        if not session:
            return None

        session.asientos_disponibles = self._calculate_available_seats(session)
        return SesionDetalleSchema.model_validate(session).model_dump(mode="json")

    def search_formatted(self, query: str, skip: int, limit: int) -> dict:
        db_sessions = self.repository.search(query=query, skip=skip, limit=limit)
        total = self.repository.count_search(query=query)

        items = []
        for session in db_sessions:
            session.asientos_disponibles = self._calculate_available_seats(session)
            items.append(SesionListadoSchema.model_validate(session).model_dump(mode="json"))

        return {"total": total, "items": items}