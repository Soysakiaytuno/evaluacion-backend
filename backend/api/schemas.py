import uuid
from datetime import datetime
from pydantic import BaseModel, Field, ConfigDict

class ConferenciaSchema(BaseModel):
    id: uuid.UUID
    name: str = Field(validation_alias="nombre")
    model_config = ConfigDict(from_attributes=True, populate_by_name=True)

class UsuarioSchema(BaseModel):
    first_name: str = Field(validation_alias="nombre")
    last_name: str = Field(validation_alias="apellido")
    model_config = ConfigDict(from_attributes=True, populate_by_name=True)

class PonenteSchema(BaseModel):
    name: str = Field(validation_alias="nombre_completo")
    affiliation: str | None = Field(None, validation_alias="descripcion")
    model_config = ConfigDict(from_attributes=True, populate_by_name=True)

class TrackSchema(BaseModel):
    id: uuid.UUID
    name: str = Field(validation_alias="nombre")
    model_config = ConfigDict(from_attributes=True, populate_by_name=True)

class SesionBase(BaseModel):
    id: uuid.UUID
    title: str = Field(validation_alias="titulo")
    abstract: str | None = Field(default=None, validation_alias="descripcion")
    starts_at: datetime = Field(validation_alias="hora_inicio")
    ends_at: datetime = Field(validation_alias="hora_fin")
    capacity: int = Field(validation_alias="capacidad")
    registered: int = Field(default=0)
    model_config = ConfigDict(from_attributes=True, populate_by_name=True)

class SesionDetalleSchema(SesionBase):
    track: TrackSchema
    speakers: list[PonenteSchema] = Field(default=[], validation_alias="ponentes")
    available_seats: int = Field(..., validation_alias="asientos_disponibles")

class SesionListadoSchema(SesionBase):
    track: TrackSchema
    speakers: list[PonenteSchema] = Field(default=[], validation_alias="ponentes")
    available_seats: int = Field(..., validation_alias="asientos_disponibles")


class PaginatedSesionResponse(BaseModel):
    count: int
    results: list[SesionListadoSchema]

class AgendaUsuario(BaseModel):
    sesiones: list[SesionBase]
    conflictos: list[SesionBase]
    total: int
    total_conflictos: int

