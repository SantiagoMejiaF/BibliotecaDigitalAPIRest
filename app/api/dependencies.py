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
from app.core.security import verify_token


def get_db_session(db: Session = Depends(get_db)):
    """
    Dependencia para obtener una sesión de base de datos.

    Args:
        db (Session): Sesión activa de SQLAlchemy.

    Returns:
        Session: Sesión de base de datos.
    """
    return db


def get_current_user(token: str, db: Session = Depends(get_db_session)):
    """
    Dependencia para obtener el usuario autenticado a partir de un token JWT.

    Args:
        token (str): Token JWT de autenticación.
        db (Session): Sesión activa de SQLAlchemy.

    Returns:
        User: Usuario autenticado.

    Raises:
        HTTPException: Si el token es inválido o el usuario no existe.
    """
    payload = verify_token(token)
    if not payload:
        raise HTTPException(status_code=401, detail="Token inválido o expirado")

    user_id = payload.get("sub")
    from app.services.user_service import UserService
    user = UserService.get_user_by_id(db, user_id)
    if not user:
        raise HTTPException(status_code=404, detail="Usuario no encontrado")

    return user
