"""
Módulo de seguridad y autenticación.

Maneja la generación y validación de tokens JWT.

Autor: Santiago Mejía Fernández
Fecha: 13/02/2025
"""

from datetime import datetime, timedelta, UTC
from typing import Optional
from jose import jwt
from jose.exceptions import JWTError
from app.core.config import settings


def create_access_token(data: dict, expires_delta: Optional[timedelta] = None):
    """
    Genera un token de acceso JWT.

    Args:
        data (dict): Datos a incluir en el token.
        expires_delta (Optional[timedelta]): Tiempo de expiración del token.

    Returns:
        str: Token JWT generado.
    """
    to_encode = data.copy()
    expire = datetime.now(UTC) + (
        expires_delta if expires_delta else timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES))  # ✅ CORRECCIÓN
    to_encode.update({"exp": expire})

    encoded_jwt = jwt.encode(to_encode, settings.SECRET_KEY, algorithm=settings.ALGORITHM)
    return encoded_jwt


def verify_token(token: str):
    """
    Verifica la validez de un token JWT.

    Args:
        token (str): Token a validar.

    Returns:
        dict: Datos del token si es válido, `None` si es inválido.
    """
    try:
        payload = jwt.decode(token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM])
        return payload
    except JWTError:
        return None
