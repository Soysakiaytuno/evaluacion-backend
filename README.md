# evaluacion-backend

Sistema de backend utilizando django y fast api para el control del backend y manejo de datos con una base de datos levantado en dockers

## Como ejecutar el proyecto

Necesitas tener lo que es docker instalado en la maquina y luego:

1. Clona el repositorio.
2. Asegúrate de tener el archivo `.env` en la raíz.
3. Ejecuta:
   `docker compose up -d --build`

**Rutas disponibles:**
- **Frontend:** http://localhost/
- **Django Admin:** http://localhost/admin/ (Usuario contraseña en `.env`)
- **FastAPI Endpoints:** http://localhost/api/v1/sessions/
- **OpenAPI Docs:** http://localhost/api/openapi.json

## 🏗️ Arquitectura y Principios SOLID (Design Decisions)

El proyecto fue diseñado separando estrictamente las responsabilidades:
- **Single Responsibility (SRP):** FastAPI no interactúa directamente con la BD. Las rutas (`routers`) delegan la lógica a la capa de `services`, y estos delegan la obtención de datos a la capa de `repository`.
- **Dependency Inversion & Injection:** Todos los servicios y repositorios se inyectan en las rutas mediante `Depends()` de FastAPI.
- **Patrones de Diseño utilizados:** 
  - *Singleton:* Para las conexiones a Postgres y Redis.
  - *Repository:* Para abstraer las consultas de SQLAlchemy (`session_repo.py`).
  - *Adapter / Alias:* Usamos `validation_alias` de Pydantic para mapear el español de la base de datos al inglés requerido por el frontend sin romper las convenciones de la base de datos.

## ⚡ Redis y Caché 

Se realizo una unica instancia al cache de readis de facil acceso, en el cual vamos a estar llenando y trayendo informacion de a poco utilizando lo que es el readis

## 🧠 Lógica de Negocio y Race Conditions

Se implementó el **Inventory / capacity enforcement**. La base de datos tiene una capacidad estática por sesión, y la API calcula los `asientos_disponibles` al vuelo restando la cantidad de oyentes inscritos (`max(0, capacidad - inscritos)`). 

## 🏁 Reflexión Final

- **De lo que estoy más orgulloso:** Siento que el modelo de base de datos implementado es bueno y a la vez simple, pudiendo cumplir principalmente el problema planteado y resolver
- **Lo que mejoraría con más tiempo:** Tal vez alguna reestructuracion de como esta manejado el fast api, siento que si bien se usaron patrones y se separaron muchas logicas pues, siento que eso se puede mejorar con un analisis de mas tiempo
>>>>>>> 740b73953db824d3889b51e670ceaff8e248e007
