"""
Esquema de validación para los tokens de sesión.

Este módulo define los modelos Pydantic utilizados para la autenticación simple.

Autor: Santiago Mejía Fernández
Fecha: 13/02/2025
"""

from datetime import datetime
from pydantic import BaseModel

class SessionTokenResponse(BaseModel):
    """
    Esquema de respuesta para el token de sesión.
    """
    access_token: str
    token_type: str = "bearer"
    created_at: datetime
