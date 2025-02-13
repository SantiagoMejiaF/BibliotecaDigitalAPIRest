"""
Esquema de validación para la entidad `User`.

Este módulo define los modelos Pydantic utilizados para la validación de datos
y la serialización en la API.

Autor: Santiago Mejía Fernández
Fecha: 13/02/2025
"""

from datetime import datetime
from pydantic import BaseModel, EmailStr

class UserBase(BaseModel):
    """
    Esquema base para la entidad User.
    Contiene los atributos comunes para creación y respuesta.
    """
    name: str
    email: EmailStr

class UserCreate(UserBase):
    """
    Esquema para la creación de un usuario.
    Hereda los atributos de `UserBase`.
    """
    pass

class UserResponse(UserBase):
    """
    Esquema de respuesta para un usuario.
    Agrega el ID y la fecha de registro.
    """
    id: int
    registered_at: datetime

    class Config:
        from_attributes = True  # Permite conversión desde modelos ORM
