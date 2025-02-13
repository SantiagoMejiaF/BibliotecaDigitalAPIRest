"""
Módulo de rutas para la gestión de préstamos y devoluciones de libros.

Define los endpoints para que los usuarios puedan tomar libros prestados
y devolverlos.

Autor: Santiago Mejía Fernández
Fecha: 13/02/2025
"""

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.services.loan_service import LoanService
from app.schemas.book import BookResponse
from app.core.database import get_db

router = APIRouter(prefix="/loans", tags=["Préstamos"])

@router.post("/borrow/{book_id}/{user_id}", response_model=BookResponse)
def borrow_book(book_id: int, user_id: int, db: Session = Depends(get_db)):
    """
    Permite a un usuario tomar prestado un libro.

    Args:
        book_id (int): ID del libro a prestar.
        user_id (int): ID del usuario que solicita el préstamo.
        db (Session): Sesión de base de datos.

    Returns:
        BookResponse: Datos del libro actualizado con la información del usuario que lo tomó prestado.

    Raises:
        HTTPException 400: Si el libro ya está prestado.
        HTTPException 404: Si el libro no existe.
    """
    book = LoanService.borrow_book(db, book_id, user_id)
    if not book:
        raise HTTPException(status_code=400, detail="El libro no está disponible para préstamo o no existe")
    return book

@router.post("/return/{book_id}", response_model=BookResponse)
def return_book(book_id: int, db: Session = Depends(get_db)):
    """
    Permite a un usuario devolver un libro prestado.

    Args:
        book_id (int): ID del libro a devolver.
        db (Session): Sesión de base de datos.

    Returns:
        BookResponse: Datos del libro actualizado sin usuario asignado.

    Raises:
        HTTPException 400: Si el libro no estaba prestado.
        HTTPException 404: Si el libro no existe.
    """
    book = LoanService.return_book(db, book_id)
    if not book:
        raise HTTPException(status_code=400, detail="El libro no estaba prestado o no existe")
    return book
