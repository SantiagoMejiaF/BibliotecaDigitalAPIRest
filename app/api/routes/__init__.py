"""
Módulo de inicialización de rutas para la API.

Este archivo organiza e importa todas las rutas de la aplicación,
permitiendo su registro centralizado en `main.py`.

Autor: Santiago Mejía Fernández
Fecha: 13/02/2025
"""

from fastapi import APIRouter
from app.api.routes.users import router as user_router
from app.api.routes.authors import router as author_router
from app.api.routes.books import router as book_router
from app.api.routes.loans import router as loan_router

# Creación del enrutador principal
api_router = APIRouter()

# Inclusión de cada módulo de rutas en el enrutador principal
api_router.include_router(user_router)
api_router.include_router(author_router)
api_router.include_router(book_router)
api_router.include_router(loan_router)

