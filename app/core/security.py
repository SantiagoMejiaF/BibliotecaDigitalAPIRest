"""
Módulo de seguridad para la autenticación simple basada en tokens de sesión.

Este módulo maneja la generación y verificación de contraseñas,
así como la generación de tokens de sesión aleatorios.

Autor: Santiago Mejía Fernández
Fecha: 13/02/2025
"""

import secrets
from passlib.context import CryptContext

# Configuración del contexto de cifrado para contraseñas
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def generate_token() -> str:
    """
    Genera un token aleatorio de 32 caracteres.

    Returns:
        str: Token de sesión generado.
    """
    return secrets.token_hex(32)

def hash_password(password: str) -> str:
    """
    Cifra una contraseña usando bcrypt.

    Args:
        password (str): La contraseña en texto plano.

    Returns:
        str: Contraseña cifrada.
    """
    return pwd_context.hash(password)

def verify_password(plain_password: str, hashed_password: str) -> bool:
    """
    Verifica si una contraseña en texto plano coincide con su hash almacenado.

    Args:
        plain_password (str): Contraseña en texto plano ingresada por el usuario.
        hashed_password (str): Hash de la contraseña almacenada en la base de datos.

    Returns:
        bool: True si la contraseña coincide, False en caso contrario.
    """
    return pwd_context.verify(plain_password, hashed_password)
