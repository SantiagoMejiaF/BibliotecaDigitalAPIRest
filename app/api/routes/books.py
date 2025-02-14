"""
Módulo de rutas para la gestión de libros.

Define los endpoints para realizar operaciones CRUD sobre la entidad `Book`.

Accesibilidad:
- **ADMINISTRADOR**: Puede crear, actualizar y eliminar libros.
- **USUARIO**: No tiene acceso a estos endpoints.

Autor: Santiago Mejía Fernández
Fecha: 13/02/2025
"""

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List, Dict, Any
from app.services.book_service import BookService
from app.schemas.book import BookCreate, BookResponse
from app.core.database import get_db
from app.api.dependencies import require_admin

# Configuración del enrutador para libros
router = APIRouter(prefix="/books", tags=["Libros"])


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


@router.post("/", response_model=BookResponse, dependencies=[Depends(require_admin)])
def create_book(book: BookCreate, db: Session = Depends(get_db)):
    """
    Crea un nuevo libro en la base de datos.

    - **Restricción:** Solo **ADMINISTRADORES** pueden crear libros.

    Args:
        book (BookCreate): Datos del nuevo libro.
        db (Session): Sesión de base de datos.

    Returns:
        BookResponse: Datos del libro creado.
    """
    return BookService.create_book(db, book)


@router.get("/", response_model=List[BookResponse], dependencies=[Depends(require_admin)])
def get_all_books(db: Session = Depends(get_db)):
    """
    Obtiene la lista de todos los libros.

    - **Restricción:** Solo **ADMINISTRADORES** pueden ver la lista de libros.

    Args:
        db (Session): Sesión de base de datos.

    Returns:
        List[BookResponse]: Lista de libros en la base de datos.
    """
    return BookService.get_all_books(db)


@router.get("/{book_id}", response_model=BookResponse, dependencies=[Depends(require_admin)])
def get_book(book_id: int, db: Session = Depends(get_db)):
    """
    Obtiene un libro por su ID.

    - **Restricción:** Solo **ADMINISTRADORES** pueden ver detalles de libros.

    Args:
        book_id (int): ID del libro a consultar.
        db (Session): Sesión de base de datos.

    Returns:
        BookResponse: Datos del libro consultado.

    Raises:
        HTTPException 404: Si el libro no existe.
    """
    book = BookService.get_book_by_id(db, book_id)
    if not book:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=error_response(404, "Libro no encontrado"))

    return book


@router.get("/search/", response_model=List[BookResponse], dependencies=[Depends(require_admin)])
def search_books(title: str = None, author: str = None, year: int = None, db: Session = Depends(get_db)):
    """
    Busca libros por título, autor o año de publicación.

    - **Restricción:** Solo **ADMINISTRADORES** pueden realizar búsquedas de libros.

    Args:
        title (str, opcional): Título del libro a buscar.
        author (str, opcional): Nombre del autor del libro.
        year (int, opcional): Año de publicación.

    Returns:
        List[BookResponse]: Lista de libros que coinciden con los criterios de búsqueda.
    """
    return BookService.search_books(db, title, author, year)


@router.put("/{book_id}", response_model=BookResponse, dependencies=[Depends(require_admin)])
def update_book(book_id: int, book: BookCreate, db: Session = Depends(get_db)):
    """
    Actualiza los datos de un libro.

    - **Restricción:** Solo **ADMINISTRADORES** pueden actualizar libros.

    Args:
        book_id (int): ID del libro a actualizar.
        book (BookCreate): Nuevos datos del libro.
        db (Session): Sesión de base de datos.

    Returns:
        BookResponse: Datos del libro actualizado.

    Raises:
        HTTPException 404: Si el libro no existe.
    """
    updated_book = BookService.update_book(db, book_id, book)
    if not updated_book:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=error_response(404, "Libro no encontrado"))

    return updated_book


@router.delete("/{book_id}", dependencies=[Depends(require_admin)])
def delete_book(book_id: int, db: Session = Depends(get_db)):
    """
    Elimina un libro de la base de datos.

    - **Restricción:** Solo **ADMINISTRADORES** pueden eliminar libros.

    Args:
        book_id (int): ID del libro a eliminar.
        db (Session): Sesión de base de datos.

    Returns:
        dict: Mensaje de éxito si el libro fue eliminado.

    Raises:
        HTTPException 404: Si el libro no existe.
    """
    success = BookService.delete_book(db, book_id)
    if not success:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=error_response(404, "Libro no encontrado"))

    return {"message": "Libro eliminado exitosamente"}
