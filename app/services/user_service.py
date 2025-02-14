"""
Servicio para la gestión de usuarios en la API.

Maneja la lógica de negocio relacionada con la entidad `User`,
incluyendo autenticación y seguridad.

Autor: Santiago Mejía Fernández
Fecha: 13/02/2025
"""

from sqlalchemy.orm import Session

from app.models import Role
from app.models.user import User
from app.models.session import SessionToken
from app.schemas.user import UserCreate, UserResponse
from app.core.security import hash_password, verify_password, generate_token

class UserService:
    """
    Clase de servicio para operaciones relacionadas con usuarios.
    """

    @staticmethod
    def create_user(db: Session, user_data: UserCreate) -> UserResponse:
        """
        Crea un nuevo usuario en la base de datos con la contraseña cifrada
        y le asigna el rol de USUARIO por defecto.

        Args:
            db (Session): Sesión de la base de datos.
            User_data (UserCreate): Datos del usuario a registrar.

        Returns:
            UserResponse: Usuario creado.
        """
        # Obtener el rol de USUARIO
        user_role = db.query(Role).filter(Role.name == "USUARIO").first()
        if not user_role:
            raise ValueError("El rol USUARIO no está creado en la base de datos")

        # Cifrar la contraseña antes de almacenarla
        hashed_password = hash_password(user_data.password)

        new_user = User(
            name=user_data.name,
            email=str(user_data.email),
            password=hashed_password,
            role_id=user_role.id
        )

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
    def get_user_by_email(db: Session, email: str) -> User | None:
        """
        Obtiene un usuario por su correo electrónico.

        Args:
            db (Session): Sesión de la base de datos.
            email (str): Correo electrónico del usuario.

        Returns:
            User | None: Usuario encontrado o `None` si no existe.
        """
        return db.query(User).filter(User.email == email).first()

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

        # Cifrar la nueva contraseña si es proporcionada
        if user_data.password:
            user.password = hash_password(user_data.password)

        user.name = user_data.name
        user.email = user_data.email

        db.commit()
        db.refresh(user)
        return UserResponse.model_validate(user)

    @staticmethod
    def delete_user(db: Session, user_id: int) -> bool:
        """
        Elimina un usuario por su ID y también borra su sesión activa.

        Args:
            db (Session): Sesión de la base de datos.
            user_id (int): ID del usuario a eliminar.

        Returns:
            bool: `True` si se eliminó, `False` si el usuario no existe.
        """
        user = db.query(User).filter(User.id == user_id).first()
        if not user:
            return False

        # Eliminar cualquier sesión activa del usuario
        db.query(SessionToken).filter(SessionToken.user_id == user.id).delete()

        db.delete(user)
        db.commit()
        return True

    @staticmethod
    def authenticate_user(db: Session, email: str, password: str) -> str | None:
        """
        Autentica a un usuario y genera un token de sesión.

        Args:
            db (Session): Sesión de la base de datos.
            email (str): Correo electrónico del usuario.
            password (str): Contraseña en texto plano.

        Returns:
            str | None: Token de sesión si la autenticación es correcta, `None` si falla.
        """
        user = UserService.get_user_by_email(db, email)
        if not user or not verify_password(password, user.password):
            return None  # Usuario no encontrado o contraseña incorrecta

        # Eliminar sesiones anteriores del usuario
        db.query(SessionToken).filter(SessionToken.user_id == user.id).delete()

        # Generar un nuevo token de sesión
        new_token = generate_token()
        session_token = SessionToken(user_id=user.id, token=new_token)

        db.add(session_token)
        db.commit()
        return new_token

    @staticmethod
    def logout_user(db: Session, user_id: int) -> bool:
        """
        Cierra la sesión del usuario eliminando su token de sesión.

        Args:
            db (Session): Sesión de la base de datos.
            user_id (int): ID del usuario.

        Returns:
            bool: `True` si se cerró sesión correctamente, `False` si no existía una sesión activa.
        """
        deleted_rows = db.query(SessionToken).filter(SessionToken.user_id == user_id).delete()
        db.commit()
        return deleted_rows > 0
