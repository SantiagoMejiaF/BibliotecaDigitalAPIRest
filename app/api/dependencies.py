"""
Módulo de dependencias compartidas para las rutas de la API.

Este archivo define funciones de dependencias que se inyectan en los endpoints
para reutilizar lógica común, como la gestión de sesiones de base de datos.

Autor: Santiago Mejía Fernández
Fecha: 13/02/2025
"""

from fastapi import Depends, HTTPException
from sqlalchemy.orm import Session
from app.core.database import get_db


def get_db_session(db: Session = Depends(get_db)):
    """
    Dependencia para obtener una sesión de base de datos.

    Args:
        db (Session): Sesión activa de SQLAlchemy.

    Returns:
        Session: Sesión de base de datos.
    """
    return db