"""
Módulo de definición del modelo `Author` para la API de la Biblioteca Digital.

Este módulo define la entidad `Author`, que representa a los autores de los libros almacenados en la biblioteca.

Autor: Santiago Mejía Fernández
Fecha: 13/02/2025
"""

from sqlalchemy import Column, Integer, String, Date
from sqlalchemy.orm import relationship
from app.core.database import Base

class Author(Base):
    """
    Modelo de Autor en la base de datos.

    Atributos:
        id (int): Identificador único del autor (autoincremental).
        name (str): Nombre del autor (obligatorio).
        birth_date (date, opcional): Fecha de nacimiento del autor.
        books (relationship): Relación con los libros escritos por el autor.
    """
    __tablename__ = "authors"

    id = Column(Integer, primary_key=True, autoincrement=True, index=True)
    name = Column(String, nullable=False)
    birth_date = Column(Date, nullable=True)

    books = relationship("Book", back_populates="author", cascade="all, delete-orphan")
