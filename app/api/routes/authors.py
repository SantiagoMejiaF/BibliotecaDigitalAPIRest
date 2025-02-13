"""
Módulo de rutas para la gestión de autores.

Define los endpoints para realizar operaciones CRUD sobre la entidad `Author`.

Autor: Santiago Mejía Fernández
Fecha: 13/02/2025
"""

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from app.services.author_service import AuthorService
from app.schemas.author import AuthorCreate, AuthorResponse
from app.core.database import get_db

router = APIRouter(prefix="/authors", tags=["Autores"])

@router.post("/", response_model=AuthorResponse)
def create_author(author: AuthorCreate, db: Session = Depends(get_db)):
    """
    Crea un nuevo autor en la base de datos.
    """
    return AuthorService.create_author(db, author)

@router.get("/", response_model=List[AuthorResponse])
def get_all_authors(db: Session = Depends(get_db)):
    """
    Obtiene la lista de todos los autores.
    """
    return AuthorService.get_all_authors(db)

@router.get("/{author_id}", response_model=AuthorResponse)
def get_author(author_id: int, db: Session = Depends(get_db)):
    """
    Obtiene un autor por su ID.
    """
    author = AuthorService.get_author_by_id(db, author_id)
    if not author:
        raise HTTPException(status_code=404, detail="Autor no encontrado")
    return author

@router.put("/{author_id}", response_model=AuthorResponse)
def update_author(author_id: int, author: AuthorCreate, db: Session = Depends(get_db)):
    """
    Actualiza los datos de un autor.
    """
    updated_author = AuthorService.update_author(db, author_id, author)
    if not updated_author:
        raise HTTPException(status_code=404, detail="Autor no encontrado")
    return updated_author

@router.delete("/{author_id}")
def delete_author(author_id: int, db: Session = Depends(get_db)):
    """
    Elimina un autor de la base de datos.
    """
    success = AuthorService.delete_author(db, author_id)
    if not success:
        raise HTTPException(status_code=404, detail="Autor no encontrado")
    return {"message": "Autor eliminado exitosamente"}
