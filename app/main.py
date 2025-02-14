"""
Punto de entrada principal de la API Biblioteca Digital.

Configura la aplicación FastAPI, registra rutas y middlewares,
y gestiona eventos de inicio y apagado con Lifespan.

Autor: Santiago Mejía Fernández
Fecha: 13/02/2025
"""

import uvicorn
from fastapi import FastAPI
from contextlib import asynccontextmanager
from fastapi.middleware.cors import CORSMiddleware
from app.api.routes import api_router
from app.core.config import settings

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
    yield
    print("🛑 API Biblioteca Digital detenida.")  # Evento de apagado

# Inicialización de la aplicación con Lifespan
app = FastAPI(
    title=settings.APP_NAME,
    description="API REST para la gestión de una biblioteca digital.",
    version="1.0.0",
    docs_url="/swagger",
    redoc_url="/documentation",
    lifespan=lifespan
)

# Registrar todas las rutas de la API
app.include_router(api_router)

# Punto de entrada para ejecutar con `python main.py`
if __name__ == "__main__":
    uvicorn.run("app.main:app", host="0.0.0.0", port=8000, reload=True)
