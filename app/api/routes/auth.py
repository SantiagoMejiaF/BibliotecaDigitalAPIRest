"""
Módulo de autenticación para la API de la Biblioteca Digital.

Define el endpoint para autenticar usuarios y generar tokens de sesión.

Accesibilidad:
- **ADMINISTRADOR**: Puede iniciar sesión.
- **USUARIO**: Puede iniciar sesión.
- **NO AUTENTICADOS**: Tienen acceso a este endpoint sin restricciones.

Autor: Santiago Mejía Fernández
Fecha: 13/02/2025
"""

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.schemas import UserResponse, UserCreate
from app.schemas.auth import LoginRequest
from app.schemas.session import SessionTokenResponse
from app.services.user_service import UserService
from app.services.session_service import SessionService
from passlib.context import CryptContext
from typing import Dict, Any

# Configuración del enrutador para autenticación
router = APIRouter(prefix="/auth", tags=["Autenticación"])

# Configuración de hashing para contraseñas
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

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

@router.post("/login", response_model=SessionTokenResponse, status_code=status.HTTP_200_OK)
def login(request: LoginRequest, db: Session = Depends(get_db)):
    """
      **Inicia sesión y genera un token de sesión.**

    - **Este endpoint está accesible para cualquier usuario sin autenticación.**
    - **Permite a ADMINISTRADORES y USUARIOS iniciar sesión.**
    - Si las credenciales son correctas, genera un token de sesión.

    ### **Parámetros**
    - `request` (**LoginRequest**): Datos de acceso (*email* y *contraseña*).
    - `db` (**Session**): Sesión de la base de datos.

    ### **Retorna**
    - **200 OK** → `SessionTokenResponse`: Token de sesión generado.
    - **401 Unauthorized** → Si las credenciales son inválidas.

    ### **Ejemplo de Respuesta Exitosa**
    ```json
    {
        "access_token": "tokengenerado123",
        "token_type": "bearer",
        "created_at": "2025-02-13T12:00:00"
    }
    ```

    ### **Ejemplo de Error**
    ```json
    {
        "status": "error",
        "status_code": 401,
        "detail": "Credenciales inválidas"
    }
    ```
    """
    # Buscar usuario por email
    user = UserService.get_user_by_email(db, str(request.email))

    # Verificar credenciales
    if user is None or not pwd_context.verify(request.password, user.password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=error_response(401, "Credenciales inválidas")
        )

    # Generar sesión
    session_token = SessionService.create_session(db, user.id)

    return {
        "access_token": session_token.token,
        "token_type": "bearer",
        "created_at": session_token.created_at
    }

@router.post("/register", response_model=UserResponse, status_code=status.HTTP_201_CREATED)
def create_user(user: UserCreate, db: Session = Depends(get_db)):
    """
    Crea un nuevo usuario en la base de datos con el rol **USUARIO** por defecto.

    - **Este endpoint está accesible para cualquier usuario sin autenticación.**
    - **Contraseña:** Se almacena cifrada.
    - **Email:** Debe ser único.

    Args:
        user (UserCreate): Datos del usuario a registrar.
        db (Session): Sesión de base de datos.

    Returns:
        UserResponse: Usuario creado con su información.

    Raises:
        HTTPException 400: Si el correo ya está registrado.
    """
    existing_user = UserService.get_user_by_email(db, str(user.email))
    if existing_user:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                            detail=error_response(400, "El correo ya está registrado"))

    return UserService.create_user(db, user)
