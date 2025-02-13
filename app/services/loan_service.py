"""
Servicio para la gestión de préstamos de libros en la API.

Maneja la lógica de negocio relacionada con el préstamo y devolución de libros.

Autor: Santiago Mejía Fernández
Fecha: 13/02/2025
"""

from sqlalchemy.orm import Session
from app.models.book import Book
from app.schemas.book import BookResponse

class LoanService:
    """
    Clase de servicio para operaciones de préstamos de libros.
    """

    @staticmethod
    def borrow_book(db: Session, book_id: int, user_id: int) -> BookResponse | None:
        """
        Registra el préstamo de un libro a un usuario.

        Args:
            db (Session): Sesión de la base de datos.
            book_id (int): ID del libro a prestar.
            user_id (int): ID del usuario que toma el libro.

        Returns:
            BookResponse | None: Libro actualizado o `None` si no se puede prestar.
        """
        book = db.query(Book).filter(Book.id == book_id).first()
        if not book or book.borrowed_by_id:
            return None  # El libro no existe o ya está prestado

        book.borrowed_by_id = user_id
        db.commit()
        db.refresh(book)
        return BookResponse.model_validate(book)

    @staticmethod
    def return_book(db: Session, book_id: int) -> BookResponse | None:
        """
        Registra la devolución de un libro.

        Args:
            db (Session): Sesión de la base de datos.
            book_id (int): ID del libro a devolver.

        Returns:
            BookResponse | None: Libro actualizado o `None` si el libro no estaba prestado.
        """
        book = db.query(Book).filter(Book.id == book_id).first()
        if not book or not book.borrowed_by_id:
            return None  # El libro no estaba prestado

        book.borrowed_by_id = None
        db.commit()
        db.refresh(book)
        return BookResponse.model_validate(book)
