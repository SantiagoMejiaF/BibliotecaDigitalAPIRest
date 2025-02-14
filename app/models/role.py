"""
Módulo de definición del modelo `Role` para la gestión de roles de usuario.

Autor: Santiago Mejía Fernández
Fecha: 13/02/2025
"""

from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship
from app.core.database import Base

class Role(Base):
    """
    Modelo de Rol en la base de datos.

    Atributos:
        id (int): Identificador único del rol.
        name (str): Nombre del rol (ADMINISTRADOR, USUARIO).
        users (relationship): Relación con la tabla `users`.
    """
    __tablename__ = "roles"

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String, unique=True, nullable=False)

    # Relación con la tabla de usuarios
    users = relationship("User", back_populates="role")

