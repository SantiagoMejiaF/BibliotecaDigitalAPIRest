"""
Módulo de definición del modelo `SessionToken` para autenticación simple.

Este modelo almacena los tokens de sesión generados en el login.

Autor: Santiago Mejía Fernández
Fecha: 13/02/2025
"""

from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, func
from sqlalchemy.orm import relationship
from app.core.database import Base

class SessionToken(Base):
    """
    Modelo de Token de Sesión para autenticación simple.

    Atributos:
        id (int): Identificador único del token.
        user_id (int): ID del usuario al que pertenece el token.
        token (str): Token generado para la sesión.
        created_at (datetime): Fecha y hora de creación del token.
    """
    __tablename__ = "session_tokens"

    id = Column(Integer, primary_key=True, autoincrement=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    token = Column(String, unique=True, nullable=False, index=True)
    created_at = Column(DateTime, server_default=func.now())

    user = relationship("User", back_populates="session")
