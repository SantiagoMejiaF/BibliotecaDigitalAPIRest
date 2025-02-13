"""
Servicio para la gestión de usuarios en la API.

Maneja la lógica de negocio relacionada con la entidad `User`.

Autor: Santiago Mejía Fernández
Fecha: 13/02/2025
"""

from sqlalchemy.orm import Session
from app.models.user import User
from app.schemas.user import UserCreate, UserResponse

class UserService:
    """
    Clase de servicio para operaciones relacionadas con usuarios.
    """

    @staticmethod
    def create_user(db: Session, user_data: UserCreate) -> UserResponse:
        """
        Crea un nuevo usuario en la base de datos.

        Args:
            db (Session): Sesión de la base de datos.
            user_data (UserCreate): Datos del usuario a registrar.

        Returns:
            UserResponse: Usuario creado.
        """
        new_user = User(**user_data.model_dump())
        db.add(new_user)
        db.commit()
        db.refresh(new_user)
        return UserResponse.model_validate(new_user)

    @staticmethod
    def get_user_by_id(db: Session, user_id: int) -> UserResponse | None:
        """
        Obtiene un usuario por su ID.

        Args:
            db (Session): Sesión de la base de datos.
            user_id (int): ID del usuario a buscar.

        Returns:
            UserResponse | None: Usuario encontrado o `None` si no existe.
        """
        user = db.query(User).filter(User.id == user_id).first()
        return UserResponse.model_validate(user) if user else None

    @staticmethod
    def get_all_users(db: Session) -> list[UserResponse]:
        """
        Obtiene la lista de todos los usuarios registrados.

        Args:
            db (Session): Sesión de la base de datos.

        Returns:
            list[UserResponse]: Lista de usuarios en la base de datos.
        """
        return [UserResponse.model_validate(user) for user in db.query(User).all()]

    @staticmethod
    def update_user(db: Session, user_id: int, user_data: UserCreate) -> UserResponse | None:
        """
        Actualiza los datos de un usuario existente.

        Args:
            db (Session): Sesión de la base de datos.
            user_id (int): ID del usuario a actualizar.
            user_data (UserCreate): Nuevos datos del usuario.

        Returns:
            UserResponse | None: Usuario actualizado o `None` si no existe.
        """
        user = db.query(User).filter(User.id == user_id).first()
        if not user:
            return None
        for key, value in user_data.model_dump().items():
            setattr(user, key, value)
        db.commit()
        db.refresh(user)
        return UserResponse.model_validate(user)

    @staticmethod
    def delete_user(db: Session, user_id: int) -> bool:
        """
        Elimina un usuario por su ID.

        Args:
            db (Session): Sesión de la base de datos.
            user_id (int): ID del usuario a eliminar.

        Returns:
            bool: `True` si se eliminó, `False` si el usuario no existe.
        """
        user = db.query(User).filter(User.id == user_id).first()
        if not user:
            return False
        db.delete(user)
        db.commit()
        return True
