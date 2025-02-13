"""
Módulo de definición del modelo `Book` para la API de la Biblioteca Digital.

Este módulo define la entidad `Book`, que representa los libros almacenados en la biblioteca y sus relaciones con autores y usuarios.

Autor: Santiago Mejía Fernández
Fecha: 13/02/2025
"""

from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from app.core.database import Base

class Book(Base):
    """
    Modelo de Libro en la base de datos.

    Atributos:
        id (int): Identificador único del libro (autoincremental).
        title (str): Título del libro (obligatorio).
        publication_year (int, opcional): Año de publicación del libro.
        author_id (int): Clave foránea que referencia al autor del libro.
        borrowed_by_id (int, opcional): Clave foránea que referencia al usuario que ha tomado prestado el libro.
        author (relationship): Relación con el autor del libro.
        borrowed_by (relationship): Relación con el usuario que tiene el libro prestado.
    """
    __tablename__ = "books"

    id = Column(Integer, primary_key=True, autoincrement=True, index=True)
    title = Column(String, nullable=False)
    publication_year = Column(Integer, nullable=True)

    author_id = Column(Integer, ForeignKey("authors.id", ondelete="CASCADE"), nullable=False)
    borrowed_by_id = Column(Integer, ForeignKey("users.id", ondelete="SET NULL"), nullable=True)

    author = relationship("Author", back_populates="books")
    borrowed_by = relationship("User", back_populates="borrowed_books", foreign_keys=[borrowed_by_id])
