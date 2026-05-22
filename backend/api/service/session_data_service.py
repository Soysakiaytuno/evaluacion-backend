import uuid
from ..repository.session_repo import SessionRepository
from ..schemas import SesionListadoSchema, SesionDetalleSchema, TrackSchema, AgendaUsuario

class SessionDataService:
    """Servicio encargado de la lógica de negocio y transformación de datos."""
    def __init__(self, repository: SessionRepository):
        self.repository = repository

    def get_tracks_formatted(self) -> list:
        tracks = self.repository.get_tracks()
        return [TrackSchema.model_validate(t).model_dump(mode="json") for t in tracks]

    def _prepare_session(self, session):
        """Prepara los campos calculados que requiere el frontend."""
        session.registered = len(session.oyentes) if session.oyentes else 0
        session.asientos_disponibles = max(0, session.capacidad - session.registered)
        for p in session.ponentes:
            p.nombre_completo = f"{p.usuario.nombre} {p.usuario.apellido}"
        return session

    def get_sessions_formatted(self, page: int, page_size: int, q: str = None, track: str = None, day: str = None, tz: str = 'UTC') -> dict:
        skip = (page - 1) * page_size
        db_sessions = self.repository.get_sessions(q=q, track_id=track, skip=skip, limit=page_size, day=day, tz=tz)
        total = self.repository.count_sessions(q=q, track_id=track, day=day, tz=tz)

        items = []
        for session in db_sessions:
            self._prepare_session(session)
            items.append(SesionListadoSchema.model_validate(session).model_dump(mode="json"))

        return {
            "count": total,
            "results": items
        }

    def get_by_id_formatted(self, session_id: uuid.UUID) -> dict | None:
        session = self.repository.get_by_id(session_id)
        if not session:
            return None

        self._prepare_session(session)
        return SesionDetalleSchema.model_validate(session).model_dump(mode="json")
    
    def get_agenda(self, oyente_id: uuid.UUID):
        agenda = self.repository.get_agenda_usuario(oyente_id)
        count_conflict: int = 0
        resultado: AgendaUsuario
        resultado.sesiones = agenda
        previo = agenda[0]
        duraciones = previo.hora_inicio + previo.hora_fin
        for sesiones in agenda:
            if previo.id != sesiones.id:
                if (previo.hora_inicio >= sesiones.hora_inicio and previo.hora_inicio <= sesiones.hora_fin) or (previo.hora_fin <= sesiones.hora_fin and previo.hora_fin >= sesiones.hora_inicio):
                    resultado.conflictos.add(sesiones)
                    resultado.conflictos.add(previo)
                    count_conflict += 1
                duraciones += (sesiones.hora_fin + sesiones.hora_fin)
                previo = sesiones
        resultado.total = duraciones
        resultado.total_conflictos = count_conflict
        return resultado