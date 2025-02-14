"""
Módulo de servicio para gestionar tokens de sesión.

Este módulo maneja la creación, validación y eliminación de tokens.

Autor: Santiago Mejía Fernández
Fecha: 13/02/2025
"""

from sqlalchemy.orm import Session
from app.models.session import SessionToken
from app.core.security import generate_token

class SessionService:
    @staticmethod
    def create_session(db: Session, user_id: int):
        """
        Crea un nuevo token de sesión para el usuario.

        Args:
            db (Session): Sesión de base de datos.
            user_id (int): ID del usuario.

        Returns:
            SessionToken: Token generado.
        """
        # Elimina tokens previos del usuario
        db.query(SessionToken).filter(SessionToken.user_id == user_id).delete()

        # Genera un nuevo token
        new_token = generate_token()
        session_token = SessionToken(user_id=user_id, token=new_token)

        db.add(session_token)
        db.commit()
        db.refresh(session_token)
        return session_token

    @staticmethod
    def get_session(db: Session, token: str):
        """
        Obtiene una sesión por su token.

        Args:
            db (Session): Sesión de base de datos.
            token (str): Token de sesión.

        Returns:
            SessionToken: Sesión si el token es válido.
        """
        return db.query(SessionToken).filter(SessionToken.token == token).first()

    @staticmethod
    def delete_session(db: Session, token: str):
        """
        Elimina un token de sesión.

        Args:
            db (Session): Sesión de base de datos.
            token (str): Token de sesión.
        """
        db.query(SessionToken).filter(SessionToken.token == token).delete()
        db.commit()
