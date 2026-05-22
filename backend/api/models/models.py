import uuid
from sqlalchemy import Column, String, Integer, Date, DateTime, ForeignKey, Text, Table
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
from ..database import Base

sesion_ponente = Table(
    'sesion_ponente',
    Base.metadata,
    Column('id_sesion', UUID(as_uuid=True), ForeignKey('content.sesion.id'), primary_key=True),
    Column('id_ponente', UUID(as_uuid=True), ForeignKey('content.ponente.id'), primary_key=True),
    schema='content'
)

class Usuario(Base):
    __tablename__ = "usuario"
    __table_args__ = {"schema": "content"}
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    nombre = Column(String(100), nullable=False)
    apellido = Column(String(100), nullable=False)

class Ponente(Base):
    __tablename__ = "ponente"
    __table_args__ = {"schema": "content"}
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    id_usuario = Column(UUID(as_uuid=True), ForeignKey('content.usuario.id'), nullable=False)
    descripcion = Column(Text)
    
    usuario = relationship("Usuario")

class Conferencia(Base):
    __tablename__ = "conferencia"
    __table_args__ = {"schema": "content"}
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    nombre = Column(String(255), nullable=False)

class Track(Base):
    __tablename__ = "track"
    __table_args__ = {"schema": "content"}
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    id_conferencia = Column(UUID(as_uuid=True), ForeignKey('content.conferencia.id'), nullable=False)
    nombre = Column(String(255), nullable=False)

class Sesion(Base):
    __tablename__ = "sesion"
    __table_args__ = {"schema": "content"}
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    id_track = Column(UUID(as_uuid=True), ForeignKey('content.track.id'), nullable=False)
    titulo = Column(String(255), nullable=False)
    descripcion = Column(Text)
    hora_inicio = Column(DateTime(timezone=True), nullable=False)
    hora_fin = Column(DateTime(timezone=True), nullable=False)
    capacidad = Column(Integer, default=50)
    
    track = relationship("Track")
    ponentes = relationship("Ponente", secondary=sesion_ponente)
    oyentes = relationship("Oyente", back_populates="sesion")

class Oyente(Base):
    __tablename__ = "oyente"
    __table_args__ = {"schema": "content"}
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    id_sesion = Column(UUID(as_uuid=True), ForeignKey('content.sesion.id'), nullable=False)
    
    sesion = relationship("Sesion", back_populates="oyentes")