import uuid
from datetime import datetime
from pydantic import BaseModel, Field, ConfigDict

class ConferenciaSchema(BaseModel):
    id: uuid.UUID
    nombre: str
    model_config = ConfigDict(from_attributes=True)

class UsuarioSchema(BaseModel):
    nombre: str
    apellido: str

    model_config = ConfigDict(from_attributes=True)

class PonenteSchema(BaseModel):
    descripcion: str | None
    usuario: UsuarioSchema

    model_config = ConfigDict(from_attributes=True)

class TrackSchema(BaseModel):
    id: uuid.UUID
    nombre: str

    model_config = ConfigDict(from_attributes=True)

class SesionBase(BaseModel):
    id: uuid.UUID
    titulo: str
    descripcion: str | None = Field(None, description="Descripción de lo que trata la sesión")
    hora_inicio: datetime
    hora_fin: datetime
    capacidad: int

class SesionDetalleSchema(SesionBase):
    track: TrackSchema
    ponentes: list[PonenteSchema] = []
    asientos_disponibles: int = Field(..., description="Cálculo en vivo: (capacidad - total de oyentes)")

    model_config = ConfigDict(from_attributes=True)

class SesionListadoSchema(SesionBase):
    track: TrackSchema
    asientos_disponibles: int = Field(..., description="Cálculo en vivo: (capacidad - total de oyentes)")

    model_config = ConfigDict(from_attributes=True)


class PaginatedSesionResponse(BaseModel):
    total: int
    page: int
    size: int
    pages: int
    items: list[SesionListadoSchema]