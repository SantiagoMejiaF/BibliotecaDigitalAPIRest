"""
Rutas para la gestión de usuarios en la API.

Maneja el CRUD de usuarios y la autenticación mediante tokens de sesión.

Se aplican restricciones de acceso según el rol del usuario:
- **ADMINISTRADOR**: Puede acceder a todos los endpoints.
- **USUARIO**: Puede acceder únicamente a `/users` y `/loans`.
- **Público**: Solo `/auth/login` y `users/register` es accesible sin autenticación.

Autor: Santiago Mejía Fernández
Fecha: 13/02/2025
"""

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List, Dict, Any
from app.services.user_service import UserService
from app.core.database import get_db
from app.schemas.user import UserCreate, UserResponse
from app.api.dependencies import get_current_user, require_admin, require_user_or_admin

# Configuración del enrutador para usuarios
router = APIRouter(prefix="/users", tags=["Usuarios"])


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


@router.get("/me", response_model=UserResponse, dependencies=[Depends(require_user_or_admin)])
def get_current_user_data(current_user: UserResponse = Depends(get_current_user)):
    """
    Obtiene la información del usuario autenticado.

    - **Restricción:** Solo el usuario autenticado puede acceder a su propia información.

    Args:
        current_user (UserResponse): Usuario autenticado.

    Returns:
        UserResponse: Datos del usuario autenticado.
    """
    return current_user


@router.get("/{user_id}", response_model=UserResponse, dependencies=[Depends(require_user_or_admin)])
def get_user(user_id: int, db: Session = Depends(get_db)):
    """
    Obtiene un usuario por su ID.

    - **Restricción:** Solo el usuario autenticado o un **ADMINISTRADOR** puede consultar usuarios.

    Args:
        user_id (int): ID del usuario a buscar.
        db (Session): Sesión de base de datos.

    Returns:
        UserResponse: Datos del usuario si existe.

    Raises:
        HTTPException 404: Si el usuario no existe.
    """
    user = UserService.get_user_by_id(db, user_id)
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=error_response(404, "Usuario no encontrado"))

    return user


@router.get("/", response_model=List[UserResponse], dependencies=[Depends(require_admin)])
def get_all_users(db: Session = Depends(get_db)):
    """
    Obtiene la lista de todos los usuarios registrados.

    - **Restricción:** Solo un **ADMINISTRADOR** puede listar todos los usuarios.

    Args:
        db (Session): Sesión de base de datos.

    Returns:
        List[UserResponse]: Lista de usuarios en la base de datos.
    """
    return UserService.get_all_users(db)


@router.put("/{user_id}", response_model=UserResponse, dependencies=[Depends(require_user_or_admin)])
def update_user(user_id: int, user: UserCreate, db: Session = Depends(get_db)):
    """
    Actualiza los datos de un usuario.

    - **Restricción:** Solo el usuario autenticado o un **ADMINISTRADOR** puede actualizar un usuario.
    - **Contraseña:** Si se actualiza, se almacena cifrada.

    Args:
        user_id (int): ID del usuario a actualizar.
        user (UserCreate): Nuevos datos del usuario.
        db (Session): Sesión de base de datos.

    Returns:
        UserResponse: Usuario actualizado.

    Raises:
        HTTPException 404: Si el usuario no existe.
    """
    updated_user = UserService.update_user(db, user_id, user)
    if not updated_user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=error_response(404, "Usuario no encontrado"))

    return updated_user


@router.delete("/{user_id}", status_code=status.HTTP_204_NO_CONTENT, dependencies=[Depends(require_admin)])
def delete_user(user_id: int, db: Session = Depends(get_db)):
    """
    Elimina un usuario de la base de datos.

    - **Restricción:** Solo un **ADMINISTRADOR** puede eliminar usuarios.

    Args:
        user_id (int): ID del usuario a eliminar.
        db (Session): Sesión de base de datos.

    Returns:
        status 204 si se eliminó correctamente.

    Raises:
        HTTPException 404: Si el usuario no existe.
    """
    success = UserService.delete_user(db, user_id)
    if not success:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=error_response(404, "Usuario no encontrado"))

    return {"message": "Usuario eliminado exitosamente"}
