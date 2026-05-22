from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from .routers import session_router
app = FastAPI()

app.include_router(session_router.router)

# Permitir CORS (útil si pruebas el frontend localmente sin Nginx)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/healthz", tags=["Health"])
@app.get("/api/v1/healthz", tags=["Health"], include_in_schema=False)
def health_check():
    return {"status": "ok"}
