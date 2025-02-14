"""
Módulo de dependencias compartidas para las rutas de la API.

Este archivo define funciones de dependencias que se inyectan en los endpoints
para reutilizar lógica común, como la gestión de sesiones de base de datos.

Autor: Santiago Mejía Fernández
Fecha: 13/02/2025
"""

from fastapi import Depends, HTTPException, status, Request
from sqlalchemy.orm import Session
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from app.core.database import get_db
from app.services.session_service import SessionService
from app.models.user import User


def get_db_session(db: Session = Depends(get_db)):
    """
    Dependencia para obtener una sesión de base de datos.

    Args:
        db (Session): Sesión activa de SQLAlchemy.

    Returns:
        Session: Sesión de base de datos.
    """
    return db

security = HTTPBearer()

def get_current_user(
        request: Request,
        db: Session = Depends(get_db),
        credentials: HTTPAuthorizationCredentials = Depends(security)
):
    """
    Verifica el token de sesión y devuelve el usuario autenticado.

    Permite acceso sin autenticación a `/docs`, `/redoc`, `/openapi.json` y `/auth/login`.
    """
    public_routes = ["/docs", "/redoc", "/openapi.json", "/auth/login"]
    if any(request.url.path.startswith(route) for route in public_routes):
        return None

    session = SessionService.get_session(db, credentials.credentials)

    if not session:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Token inválido o expirado")

    return session.user  # ✅ Retornar usuario autenticado


def require_admin(current_user: User = Depends(get_current_user)):
    """
    Verifica que el usuario autenticado tenga el rol de ADMINISTRADOR.
    """
    if not current_user or current_user.role.name != "ADMINISTRADOR":
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
                            detail="Acceso denegado: Se requiere el rol de ADMINISTRADOR")
    return current_user


def require_user_or_admin(current_user: User = Depends(get_current_user)):
    """
    Verifica que el usuario autenticado tenga el rol de USUARIO o ADMINISTRADOR.
    """
    if not current_user or current_user.role.name not in ["USUARIO", "ADMINISTRADOR"]:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Acceso denegado")
    return current_user
