import uuid
from fastapi import APIRouter, Depends, Query, HTTPException
from ..schemas import PaginatedSesionResponse, SesionDetalleSchema
from ..dependencies import get_session_service
from ..service.session_service import SessionService

router = APIRouter(prefix="/api/v1", tags=["Sessions"])

@router.get("/tracks/")
def list_tracks(service: SessionService = Depends(get_session_service)):
    """Devuelve la lista de tracks para los filtros del frontend."""
    return service.get_tracks()

@router.get("/sessions", response_model=PaginatedSesionResponse, include_in_schema=False)
@router.get("/sessions/", response_model=PaginatedSesionResponse)
def list_sessions(
    page: int = Query(1, ge=1), 
    page_size: int = Query(12, ge=1, le=100), 
    q: str = None, track: str = None, day: str = None, tz: str = None,
    service: SessionService = Depends(get_session_service)
):
    """Lista y busca sesiones de forma paginada y filtrada."""
    return service.get_sessions(page=page, page_size=page_size, q=q, track=track, day=day, tz=tz)

@router.get("/sessions/{session_id}", response_model=SesionDetalleSchema)
def get_session(session_id: uuid.UUID, service: SessionService = Depends(get_session_service)):
    """Obtiene el detalle completo de una sesión con el cálculo en vivo de asientos."""
    result = service.get_by_id(session_id)
    if not result:
        raise HTTPException(status_code=404, detail="Sesión no encontrada")
    return result

@router.get("/users/{id}/agenda")
def get_agenda(id: uuid.UUID, service: SessionService = Depends(get_session_service)):
    result = service.get_agenda(id)
    if not result:
        raise HTTPException(status_code=404, detail="Sesión no encontrada")
    return result