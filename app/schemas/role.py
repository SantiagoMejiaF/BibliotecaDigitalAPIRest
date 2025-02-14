"""
Esquema de validación para la entidad `Role`.

Este módulo define los modelos Pydantic utilizados para la validación de roles
y la asignación de permisos en la API.

Autor: Santiago Mejía Fernández
Fecha: 13/02/2025
"""

from pydantic import BaseModel
from enum import Enum

class RoleEnum(str, Enum):
    """
    Enumeración de los roles disponibles en la API.

    - **ADMINISTRADOR**: Puede acceder a todos los endpoints.
    - **USUARIO**: Puede acceder únicamente a endpoints limitados.
    """
    ADMINISTRADOR = "ADMINISTRADOR"
    USUARIO = "USUARIO"

class RoleBase(BaseModel):
    """
    Esquema base para la entidad Role.
    Define los atributos comunes entre la creación y respuesta.
    """
    name: RoleEnum

class RoleResponse(RoleBase):
    """
    Esquema de respuesta para un rol.
    """
    id: int

    class Config:
        from_attributes = True  # Permite conversión desde modelos ORM.
