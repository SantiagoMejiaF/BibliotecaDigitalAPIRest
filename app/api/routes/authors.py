"""
Módulo de rutas para la gestión de autores.

Define los endpoints para realizar operaciones CRUD sobre la entidad `Author`.

Accesibilidad:
- **ADMINISTRADOR**: Puede crear, actualizar y eliminar autores.
- **USUARIO**: No tiene acceso a estos endpoints.

Autor: Santiago Mejía Fernández
Fecha: 13/02/2025
"""

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List, Dict, Any
from app.services.author_service import AuthorService
from app.schemas.author import AuthorCreate, AuthorResponse
from app.core.database import get_db
from app.api.dependencies import require_admin

# Configuración del enrutador para autores
router = APIRouter(prefix="/authors", tags=["Autores"])

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

@router.post("/", response_model=AuthorResponse, dependencies=[Depends(require_admin)])
def create_author(author: AuthorCreate, db: Session = Depends(get_db)):
    """
    Crea un nuevo autor en la base de datos.

    - **Restricción:** Solo **ADMINISTRADORES** pueden crear autores.

    Args:
        author (AuthorCreate): Datos del nuevo autor.
        db (Session): Sesión de base de datos.

    Returns:
        AuthorResponse: Datos del autor creado.
    """
    return AuthorService.create_author(db, author)

@router.get("/", response_model=List[AuthorResponse], dependencies=[Depends(require_admin)])
def get_all_authors(db: Session = Depends(get_db)):
    """
    Obtiene la lista de todos los autores.

    - **Restricción:** Solo **ADMINISTRADORES** pueden ver la lista de autores.

    Args:
        db (Session): Sesión de base de datos.

    Returns:
        List[AuthorResponse]: Lista de autores en la base de datos.
    """
    return AuthorService.get_all_authors(db)

@router.get("/{author_id}", response_model=AuthorResponse, dependencies=[Depends(require_admin)])
def get_author(author_id: int, db: Session = Depends(get_db)):
    """
    Obtiene un autor por su ID.

    - **Restricción:** Solo **ADMINISTRADORES** pueden ver detalles de autores.

    Args:
        author_id (int): ID del autor a consultar.
        db (Session): Sesión de base de datos.

    Returns:
        AuthorResponse: Datos del autor consultado.

    Raises:
        HTTPException 404: Si el autor no existe.
    """
    author = AuthorService.get_author_by_id(db, author_id)
    if not author:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=error_response(404, "Autor no encontrado"))

    return author

@router.put("/{author_id}", response_model=AuthorResponse, dependencies=[Depends(require_admin)])
def update_author(author_id: int, author: AuthorCreate, db: Session = Depends(get_db)):
    """
    Actualiza los datos de un autor.

    - **Restricción:** Solo **ADMINISTRADORES** pueden actualizar autores.

    Args:
        author_id (int): ID del autor a actualizar.
        author (AuthorCreate): Nuevos datos del autor.
        db (Session): Sesión de base de datos.

    Returns:
        AuthorResponse: Datos del autor actualizado.

    Raises:
        HTTPException 404: Si el autor no existe.
    """
    updated_author = AuthorService.update_author(db, author_id, author)
    if not updated_author:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=error_response(404, "Autor no encontrado"))

    return updated_author

@router.delete("/{author_id}", dependencies=[Depends(require_admin)])
def delete_author(author_id: int, db: Session = Depends(get_db)):
    """
    Elimina un autor de la base de datos.

    - **Restricción:** Solo **ADMINISTRADORES** pueden eliminar autores.

    Args:
        author_id (int): ID del autor a eliminar.
        db (Session): Sesión de base de datos.

    Returns:
        dict: Mensaje de éxito si el autor fue eliminado.

    Raises:
        HTTPException 404: Si el autor no existe.
    """
    success = AuthorService.delete_author(db, author_id)
    if not success:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=error_response(404, "Autor no encontrado"))

    return {"message": "Autor eliminado exitosamente"}
