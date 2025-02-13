"""
Módulo de configuración de la aplicación.

Carga las variables de entorno y define los ajustes globales de la API.

Autor: Santiago Mejía Fernández
Fecha: 13/02/2025
"""

from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    """
    Configuración de la aplicación utilizando Pydantic.

    Atributos:
        DATABASE_URL (str): URL de la base de datos.
        SECRET_KEY (str): Clave secreta para la autenticación JWT.
        ALGORITHM (str): Algoritmo usado para encriptación JWT.
        ACCESS_TOKEN_EXPIRE_MINUTES (int): Tiempo de expiración de tokens en minutos.
    """
    DATABASE_URL: str = "sqlite:///./database.db"  # Base de datos por defecto
    SECRET_KEY: str = "supersecretkey"
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60  # 1 hora

    class Config:
        env_file = ".env"  # Carga variables desde el archivo .env

settings = Settings()
