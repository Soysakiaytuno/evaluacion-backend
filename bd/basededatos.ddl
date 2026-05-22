CREATE SCHEMA IF NOT EXISTS content;

-- Extensión necesaria para generar UUIDs automáticamente
CREATE EXTENSION IF NOT EXISTS "uuid-ossp";

-- Tabla de Usuarios
CREATE TABLE content.usuario (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    nombre VARCHAR(100) NOT NULL,
    apellido VARCHAR(100) NOT NULL,
    fecha_creacion TIMESTAMPTZ DEFAULT NOW(),
    fecha_modificacion TIMESTAMPTZ DEFAULT NOW()
);

-- Tabla de Conferencias
CREATE TABLE content.conferencia (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    nombre VARCHAR(255) NOT NULL,
    fecha_inicio DATE NOT NULL,
    fecha_fin DATE NOT NULL,
    fecha_creacion TIMESTAMPTZ DEFAULT NOW(),
    fecha_modificacion TIMESTAMPTZ DEFAULT NOW()
);

-- Tabla de Tracks
CREATE TABLE content.track (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    id_conferencia UUID NOT NULL REFERENCES content.conferencia(id) ON DELETE CASCADE,
    nombre VARCHAR(255) NOT NULL,
    fecha_creacion TIMESTAMPTZ DEFAULT NOW(),
    fecha_modificacion TIMESTAMPTZ DEFAULT NOW()
);

-- Tabla de Ponentes
CREATE TABLE content.ponente (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    id_usuario UUID UNIQUE NOT NULL REFERENCES content.usuario(id) ON DELETE CASCADE,
    descripcion TEXT,
    fecha_creacion TIMESTAMPTZ DEFAULT NOW(),
    fecha_modificacion TIMESTAMPTZ DEFAULT NOW()
);

-- Tabla de Sesiones
CREATE TABLE content.sesion (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    id_track UUID NOT NULL REFERENCES content.track(id) ON DELETE CASCADE,
    titulo VARCHAR(255) NOT NULL,
    descripcion TEXT,
    hora_inicio TIMESTAMPTZ NOT NULL,
    hora_fin TIMESTAMPTZ NOT NULL,
    capacidad INTEGER NOT NULL DEFAULT 50,
    fecha_creacion TIMESTAMPTZ DEFAULT NOW(),
    fecha_modificacion TIMESTAMPTZ DEFAULT NOW()
);

-- Tabla de Oyentes
CREATE TABLE content.oyente (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    id_usuario UUID NOT NULL REFERENCES content.usuario(id) ON DELETE CASCADE,
    id_sesion UUID NOT NULL REFERENCES content.sesion(id) ON DELETE CASCADE,
    fecha_creacion TIMESTAMPTZ DEFAULT NOW(),
    fecha_modificacion TIMESTAMPTZ DEFAULT NOW(),
    CONSTRAINT unique_oyente_sesion UNIQUE (id_usuario, id_sesion)
);

-- Tabla Intermedia: Sesion <-> Ponente
CREATE TABLE content.sesion_ponente (
    id_sesion UUID NOT NULL REFERENCES content.sesion(id) ON DELETE CASCADE,
    id_ponente UUID NOT NULL REFERENCES content.ponente(id) ON DELETE CASCADE,
    PRIMARY KEY (id_sesion, id_ponente)
);