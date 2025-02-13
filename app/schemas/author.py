"""
Esquema de validación para la entidad `Author`.

Este módulo define los modelos Pydantic utilizados para la validación de datos
y la serialización en la API.

Autor: Santiago Mejía Fernández
Fecha: 13/02/2025
"""

from datetime import date
from pydantic import BaseModel
from typing import Optional

class AuthorBase(BaseModel):
    """
    Esquema base para la entidad Author.
    Contiene los atributos comunes.
    """
    name: str
    birth_date: Optional[date] = None  # Fecha opcional

class AuthorCreate(AuthorBase):
    """
    Esquema para la creación de un autor.
    Hereda los atributos de `AuthorBase`.
    """
    pass

class AuthorResponse(AuthorBase):
    """
    Esquema de respuesta para un autor.
    Agrega el ID.
    """
    id: int

    class Config:
        from_attributes = True
