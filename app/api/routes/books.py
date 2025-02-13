"""
Módulo de rutas para la gestión de libros.

Define los endpoints para realizar operaciones CRUD sobre la entidad `Book`.

Autor: Santiago Mejía Fernández
Fecha: 13/02/2025
"""

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from app.services.book_service import BookService
from app.schemas.book import BookCreate, BookResponse
from app.core.database import get_db

router = APIRouter(prefix="/books", tags=["Libros"])

@router.post("/", response_model=BookResponse)
def create_book(book: BookCreate, db: Session = Depends(get_db)):
    """
    Crea un nuevo libro en la base de datos.
    """
    return BookService.create_book(db, book)

@router.get("/", response_model=List[BookResponse])
def get_all_books(db: Session = Depends(get_db)):
    """
    Obtiene la lista de todos los libros.
    """
    return BookService.get_all_books(db)

@router.get("/{book_id}", response_model=BookResponse)
def get_book(book_id: int, db: Session = Depends(get_db)):
    """
    Obtiene un libro por su ID.
    """
    book = BookService.get_book_by_id(db, book_id)
    if not book:
        raise HTTPException(status_code=404, detail="Libro no encontrado")
    return book

@router.get("/search/", response_model=List[BookResponse])
def search_books(title: str = None, author: str = None, year: int = None, db: Session = Depends(get_db)):
    """
    Busca libros por título, autor o año de publicación.
    """
    return BookService.search_books(db, title, author, year)

@router.put("/{book_id}", response_model=BookResponse)
def update_book(book_id: int, book: BookCreate, db: Session = Depends(get_db)):
    """
    Actualiza los datos de un libro.
    """
    updated_book = BookService.update_book(db, book_id, book)
    if not updated_book:
        raise HTTPException(status_code=404, detail="Libro no encontrado")
    return updated_book

@router.delete("/{book_id}")
def delete_book(book_id: int, db: Session = Depends(get_db)):
    """
    Elimina un libro de la base de datos.
    """
    success = BookService.delete_book(db, book_id)
    if not success:
        raise HTTPException(status_code=404, detail="Libro no encontrado")
    return {"message": "Libro eliminado exitosamente"}
