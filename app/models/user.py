"""
Módulo de definición del modelo `User` para la API de la Biblioteca Digital.

Este módulo define la entidad `User`, que representa a los usuarios registrados en el sistema.
Cada usuario puede tener múltiples libros prestados.

Autor: Santiago Mejía Fernández
Fecha: 13/02/2025
"""

from sqlalchemy import Column, Integer, String, DateTime, func
from sqlalchemy.orm import relationship
from app.core.database import Base

class User(Base):
    """
    Modelo de Usuario en la base de datos.

    Atributos:
        id (int): Identificador único del usuario (autoincremental).
        name (str): Nombre del usuario (obligatorio).
        email (str): Correo electrónico del usuario (único y obligatorio).
        password (str): Contraseña cifrada del usuario (obligatorio).
        registered_at (datetime): Fecha de registro (se establece automáticamente).
        borrowed_books (relationship): Relación con los libros prestados al usuario.
    """
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, autoincrement=True, index=True)
    name = Column(String, nullable=False)
    email = Column(String, unique=True, nullable=False, index=True)
    password = Column(String, nullable=False)
    registered_at = Column(DateTime, server_default=func.now())

    borrowed_books = relationship("Book", back_populates="borrowed_by")
