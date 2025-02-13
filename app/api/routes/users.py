"""
Módulo de rutas para la gestión de usuarios.

Define los endpoints para realizar operaciones CRUD sobre la entidad `User`.

Autor: Santiago Mejía Fernández
Fecha: 13/02/2025
"""

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from app.services.user_service import UserService
from app.schemas.user import UserCreate, UserResponse
from app.core.database import get_db

router = APIRouter(prefix="/users", tags=["Usuarios"])

@router.post("/", response_model=UserResponse)
def create_user(user: UserCreate, db: Session = Depends(get_db)):
    """
    Crea un nuevo usuario en la base de datos.

    Args:
        user (UserCreate): Datos del usuario a registrar.
        db (Session): Sesión de base de datos.

    Returns:
        UserResponse: Usuario creado.
    """
    return UserService.create_user(db, user)

@router.get("/", response_model=List[UserResponse])
def get_all_users(db: Session = Depends(get_db)):
    """
    Obtiene la lista de todos los usuarios.

    Args:
        db (Session): Sesión de base de datos.

    Returns:
        List[UserResponse]: Lista de usuarios registrados.
    """
    return UserService.get_all_users(db)

@router.get("/{user_id}", response_model=UserResponse)
def get_user(user_id: int, db: Session = Depends(get_db)):
    """
    Obtiene un usuario por su ID.

    Args:
        user_id (int): ID del usuario.
        db (Session): Sesión de base de datos.

    Returns:
        UserResponse: Datos del usuario si existe.
    """
    user = UserService.get_user_by_id(db, user_id)
    if not user:
        raise HTTPException(status_code=404, detail="Usuario no encontrado")
    return user

@router.put("/{user_id}", response_model=UserResponse)
def update_user(user_id: int, user: UserCreate, db: Session = Depends(get_db)):
    """
    Actualiza los datos de un usuario.

    Args:
        user_id (int): ID del usuario a actualizar.
        user (UserCreate): Nuevos datos del usuario.
        db (Session): Sesión de base de datos.

    Returns:
        UserResponse: Usuario actualizado.
    """
    updated_user = UserService.update_user(db, user_id, user)
    if not updated_user:
        raise HTTPException(status_code=404, detail="Usuario no encontrado")
    return updated_user

@router.delete("/{user_id}")
def delete_user(user_id: int, db: Session = Depends(get_db)):
    """
    Elimina un usuario de la base de datos.

    Args:
        user_id (int): ID del usuario a eliminar.
        db (Session): Sesión de base de datos.

    Returns:
        dict: Mensaje de éxito o error.
    """
    success = UserService.delete_user(db, user_id)
    if not success:
        raise HTTPException(status_code=404, detail="Usuario no encontrado")
    return {"message": "Usuario eliminado exitosamente"}
