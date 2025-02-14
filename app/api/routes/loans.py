"""
Módulo de rutas para la gestión de préstamos y devoluciones de libros.

Define los endpoints para que los usuarios puedan tomar libros prestados
y devolverlos.

Accesibilidad:
- **ADMINISTRADOR**: Puede prestar y devolver libros.
- **USUARIO**: Puede prestar y devolver libros.

Autor: Santiago Mejía Fernández
Fecha: 13/02/2025
"""

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import Dict, Any
from app.services.loan_service import LoanService
from app.schemas.book import BookResponse
from app.core.database import get_db
from app.api.dependencies import require_user_or_admin

# Configuración del enrutador para préstamos
router = APIRouter(prefix="/loans", tags=["Préstamos"])

# Respuesta unificada para errores
def error_response(status_code: int, message: str) -> Dict[str, Any]:
    """
    Genera una respuesta de error estandarizada.

    Args:
        status_code (int): Código HTTP del error.
        message (str): Mensaje descriptivo del error.

    Returns:
        Dict[str, Any]: Diccionario con la estructura del error.
    """
    return {
        "status": "error",
        "status_code": status_code,
        "detail": message
    }

@router.post("/borrow/{book_id}/{user_id}", response_model=BookResponse, dependencies=[Depends(require_user_or_admin)])
def borrow_book(book_id: int, user_id: int, db: Session = Depends(get_db)):
    """
    Permite a un usuario o administrador tomar prestado un libro.

    - **Restricción:** Solo **USUARIOS** y **ADMINISTRADORES** pueden tomar libros en préstamo.
    - **Disponibilidad:** Un libro solo puede ser prestado si no está en uso.

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
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=error_response(400, "El libro no está disponible para préstamo o no existe"))

    return book

@router.post("/return/{book_id}", response_model=BookResponse, dependencies=[Depends(require_user_or_admin)])
def return_book(book_id: int, db: Session = Depends(get_db)):
    """
    Permite a un usuario o administrador devolver un libro prestado.

    - **Restricción:** Solo **USUARIOS** y **ADMINISTRADORES** pueden devolver libros.
    - **Disponibilidad:** Solo se pueden devolver libros que están actualmente prestados.

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
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=error_response(400, "El libro no estaba prestado o no existe"))

    return book
