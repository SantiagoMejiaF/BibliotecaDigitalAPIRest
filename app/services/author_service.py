"""
Servicio para la gestión de autores en la API.

Maneja la lógica de negocio relacionada con la entidad `Author`.

Autor: Santiago Mejía Fernández
Fecha: 13/02/2025
"""

from sqlalchemy.orm import Session
from app.models.author import Author
from app.schemas.author import AuthorCreate, AuthorResponse

class AuthorService:
    """
    Clase de servicio para operaciones relacionadas con autores.
    """

    @staticmethod
    def create_author(db: Session, author_data: AuthorCreate) -> AuthorResponse:
        """
        Crea un nuevo autor en la base de datos.

        Args:
            db (Session): Sesión de la base de datos.
            author_data (AuthorCreate): Datos del autor a registrar.

        Returns:
            AuthorResponse: Autor creado.
        """
        new_author = Author(**author_data.model_dump())
        db.add(new_author)
        db.commit()
        db.refresh(new_author)
        return AuthorResponse.model_validate(new_author)

    @staticmethod
    def get_author_by_id(db: Session, author_id: int) -> AuthorResponse | None:
        """
        Obtiene un autor por su ID.

        Args:
            db (Session): Sesión de la base de datos.
            author_id (int): ID del autor a buscar.

        Returns:
            AuthorResponse | None: Autor encontrado o `None` si no existe.
        """
        author = db.query(Author).filter(Author.id == author_id).first()
        return AuthorResponse.model_validate(author) if author else None

    @staticmethod
    def get_all_authors(db: Session) -> list[AuthorResponse]:
        """
        Obtiene la lista de todos los autores registrados.

        Args:
            db (Session): Sesión de la base de datos.

        Returns:
            list[AuthorResponse]: Lista de autores en la base de datos.
        """
        return [AuthorResponse.model_validate(author) for author in db.query(Author).all()]

    @staticmethod
    def update_author(db: Session, author_id: int, author_data: AuthorCreate) -> AuthorResponse | None:
        """
        Actualiza los datos de un autor existente.

        Args:
            db (Session): Sesión de la base de datos.
            author_id (int): ID del autor a actualizar.
            author_data (AuthorCreate): Nuevos datos del autor.

        Returns:
            AuthorResponse | None: Autor actualizado o `None` si no existe.
        """
        author = db.query(Author).filter(Author.id == author_id).first()
        if not author:
            return None
        for key, value in author_data.model_dump().items():
            setattr(author, key, value)
        db.commit()
        db.refresh(author)
        return AuthorResponse.model_validate(author)

    @staticmethod
    def delete_author(db: Session, author_id: int) -> bool:
        """
        Elimina un autor por su ID.

        Args:
            db (Session): Sesión de la base de datos.
            author_id (int): ID del autor a eliminar.

        Returns:
            bool: `True` si se eliminó, `False` si el autor no existe.
        """
        author = db.query(Author).filter(Author.id == author_id).first()
        if not author:
            return False
        db.delete(author)
        db.commit()
        return True
