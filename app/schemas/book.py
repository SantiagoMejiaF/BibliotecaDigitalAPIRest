"""
Esquema de validación para la entidad `Book`.

Este módulo define los modelos Pydantic utilizados para la validación de datos
y la serialización en la API.

Autor: Santiago Mejía Fernández
Fecha: 13/02/2025
"""

from typing import Optional
from pydantic import BaseModel

class BookBase(BaseModel):
    """
    Esquema base para la entidad Book.
    Contiene los atributos comunes.
    """
    title: str
    publication_year: Optional[int] = None
    author_id: int

class BookCreate(BookBase):
    """
    Esquema para la creación de un libro.
    Hereda los atributos de `BookBase`.
    """
    pass

class BookResponse(BookBase):
    """
    Esquema de respuesta para un libro.
    Agrega el ID y el usuario al que está prestado.
    """
    id: int
    borrowed_by_id: Optional[int] = None

    class Config:
        from_attributes = True
