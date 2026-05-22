from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI(
    title="Conferences API",
    description="API pública para consultar conferencias, tracks y sesiones.",
    version="1.0.0"
)

# Permitir CORS (útil si pruebas el frontend localmente sin Nginx)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/healthz", tags=["Health"])
def health_check():
    """
    Endpoint requerido por el Examen (3.7) para verificar la salud del contenedor.
    """
    return {"status": "ok"}
