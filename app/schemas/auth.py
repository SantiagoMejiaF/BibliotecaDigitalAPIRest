"""
Esquema de validación para autenticación de usuarios.

Define los modelos Pydantic para login y tokens.

Autor: Santiago Mejía Fernández
Fecha: 13/02/2025
"""

from pydantic import BaseModel, EmailStr

class LoginRequest(BaseModel):
    """
    Esquema para validar las credenciales de inicio de sesión.
    """
    email: EmailStr
    password: str

class TokenResponse(BaseModel):
    """
    Esquema de respuesta al autenticarse con éxito.
    """
    access_token: str
    token_type: str
