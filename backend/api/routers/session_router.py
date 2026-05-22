import uuid
from fastapi import APIRouter, Depends, Query, HTTPException
from ..schemas import PaginatedSesionResponse, SesionDetalleSchema
from ..dependencies import get_session_service
from ..service.session_service import SessionService

router = APIRouter(prefix="/api/v1/sessions", tags=["Sessions"])

@router.get("/", response_model=PaginatedSesionResponse)
def list_sessions(skip: int = Query(0, ge=0), limit: int = Query(10, le=100), service: SessionService = Depends(get_session_service)):
    """Lista todas las sesiones de forma paginada y desde caché si es posible."""
    return service.get_all(skip=skip, limit=limit)

@router.get("/search/", response_model=PaginatedSesionResponse)
def search_sessions(query: str, skip: int = 0, limit: int = 10, service: SessionService = Depends(get_session_service)):
    """Busca sesiones por título o descripción."""
    return service.search(query=query, skip=skip, limit=limit)

@router.get("/{session_id}", response_model=SesionDetalleSchema)
def get_session(session_id: uuid.UUID, service: SessionService = Depends(get_session_service)):
    """Obtiene el detalle completo de una sesión con el cálculo en vivo de asientos."""
    result = service.get_by_id(session_id)
    if not result:
        raise HTTPException(status_code=404, detail="Sesión no encontrada")
    return result