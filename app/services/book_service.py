"""
Servicio para la gestión de libros en la API.

Maneja la lógica de negocio relacionada con la entidad `Book`.

Autor: Santiago Mejía Fernández
Fecha: 13/02/2025
"""

from app.schemas.book import BookCreate, BookResponse
from sqlalchemy.orm import Session
from sqlalchemy import and_
from typing import List, Optional
from app.models.book import Book
from app.models.author import Author
from app.schemas.book import BookResponse

class BookService:
    """
    Clase de servicio para operaciones relacionadas con libros.
    """

    @staticmethod
    def create_book(db: Session, book_data: BookCreate) -> BookResponse:
        """
        Crea un nuevo libro en la base de datos.

        Args:
            db (Session): Sesión de la base de datos.
            book_data (BookCreate): Datos del libro a registrar.

        Returns:
            BookResponse: Libro creado.
        """
        new_book = Book(**book_data.model_dump())
        db.add(new_book)
        db.commit()
        db.refresh(new_book)
        return BookResponse.model_validate(new_book)

    @staticmethod
    def get_book_by_id(db: Session, book_id: int) -> BookResponse | None:
        """
        Obtiene un libro por su ID.

        Args:
            db (Session): Sesión de la base de datos.
            book_id (int): ID del libro a buscar.

        Returns:
            BookResponse | None: Libro encontrado o `None` si no existe.
        """
        book = db.query(Book).filter(Book.id == book_id).first()
        return BookResponse.model_validate(book) if book else None

    @staticmethod
    def get_all_books(db: Session) -> List[BookResponse]:
        """
        Obtiene la lista de todos los libros registrados.

        Args:
            db (Session): Sesión de la base de datos.

        Returns:
            List[BookResponse]: Lista de libros en la base de datos.
        """
        return [BookResponse.model_validate(book) for book in db.query(Book).all()]

    @staticmethod
    def update_book(db: Session, book_id: int, book_data: BookCreate) -> BookResponse | None:
        """
        Actualiza los datos de un libro existente.

        Args:
            db (Session): Sesión de la base de datos.
            book_id (int): ID del libro a actualizar.
            book_data (BookCreate): Nuevos datos del libro.

        Returns:
            BookResponse | None: Libro actualizado o `None` si no existe.
        """
        book = db.query(Book).filter(Book.id == book_id).first()
        if not book:
            return None
        for key, value in book_data.model_dump().items():
            setattr(book, key, value)
        db.commit()
        db.refresh(book)
        return BookResponse.model_validate(book)

    @staticmethod
    def delete_book(db: Session, book_id: int) -> bool:
        """
        Elimina un libro por su ID.

        Args:
            db (Session): Sesión de la base de datos.
            book_id (int): ID del libro a eliminar.

        Returns:
            bool: `True` si se eliminó, `False` si el libro no existe.
        """
        book = db.query(Book).filter(Book.id == book_id).first()
        if not book:
            return False
        db.delete(book)
        db.commit()
        return True

    @staticmethod
    def search_books(db: Session, title: Optional[str] = None, author: Optional[str] = None, year: Optional[int] = None) -> List[BookResponse]:
        """
        Busca libros en la base de datos con filtros dinámicos.

        Permite buscar libros por título, nombre del autor o año de publicación.
        Los parámetros son opcionales y pueden combinarse para refinar la búsqueda.

        Args:
            db (Session): Sesión de la base de datos.
            title (Optional[str]): Título del libro (búsqueda parcial).
            author (Optional[str]): Nombre del autor (búsqueda parcial).
            year (Optional[int]): Año de publicación del libro.

        Returns:
            List[BookResponse]: Lista de libros que coinciden con los filtros aplicados.
        """

        query = db.query(Book)

        filters = []
        if title:
            filters.append(Book.title.ilike(f"%{title}%"))  # Búsqueda insensible a mayúsculas/minúsculas
        if author:
            filters.append(Author.name.ilike(f"%{author}%"))  # Búsqueda en la tabla de autores
        if year:
            filters.append(Book.publication_year == year)

        if filters:
            query = query.join(Author).filter(and_(*filters))  # Aplicar filtros dinámicos

        books = query.all()
        return [BookResponse.model_validate(book) for book in books]
