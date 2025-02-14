"""
Punto de entrada principal de la API Biblioteca Digital.

Configura la aplicación FastAPI, registra rutas y middlewares,
y gestiona eventos de inicio y apagado con Lifespan.

Autor: Santiago Mejía Fernández
Fecha: 13/02/2025
"""

import uvicorn
from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi.security import HTTPBearer
from app.api.routes import api_router
from app.core.config import settings
from app.core.database import init_db

@asynccontextmanager
async def lifespan(app: FastAPI):
    """
    Manejador de ciclo de vida de la aplicación.

    Se ejecuta antes de que la API reciba solicitudes y al cerrar la API.

    - Se puede utilizar para inicializar conexiones a bases de datos,
      configurar caches, cargar datos iniciales, etc.
    - Al salir, permite cerrar conexiones y liberar recursos.

    Args:
        app (FastAPI): Instancia de la aplicación FastAPI.

    Yields:
        None
    """
    print("🚀 API Biblioteca Digital iniciada con éxito.")  # Evento de inicio
    init_db()
    yield
    print("🛑 API Biblioteca Digital detenida.")  # Evento de apagado

# Configuración de autenticación en Swagger
security = HTTPBearer()

app = FastAPI(
    title=settings.APP_NAME,
    description="API REST para la gestión de una biblioteca digital.",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc",
    lifespan=lifespan
)
# Registrar todas las rutas
app.include_router(api_router)

# Registrar todas las rutas de la API
app.include_router(api_router)

# Punto de entrada para ejecutar con `python main.py`
if __name__ == "__main__":
    uvicorn.run("app.main:app", host="0.0.0.0", port=8000, reload=True)
