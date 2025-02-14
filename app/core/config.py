"""
Configuración de la aplicación utilizando Pydantic Settings.

Carga las variables de entorno desde `.env` y define parámetros globales.

Autor: Santiago Mejía Fernández
Fecha: 13/02/2025
"""

from pydantic_settings import BaseSettings, SettingsConfigDict
import os
from dotenv import load_dotenv

# Cargar manualmente las variables de entorno desde .env
load_dotenv()

class Settings(BaseSettings):
    """
    Configuración de la aplicación utilizando Pydantic Settings.

    Atributos:
        APP_NAME (str): Nombre de la aplicación.
        DEBUG (bool): Modo depuración.
        DATABASE_URL (str): URL de la base de datos.
        SECRET_KEY (str): Clave secreta para autenticación JWT.
        ALGORITHM (str): Algoritmo usado en la autenticación.
        ACCESS_TOKEN_EXPIRE_MINUTES (int): Tiempo de expiración de tokens en minutos.
    """
    APP_NAME: str = os.getenv("APP_NAME", "BibliotecaDigitalAPI")
    DEBUG: bool = os.getenv("DEBUG", "True").lower() == "true"
    DATABASE_URL: str = os.getenv("DATABASE_URL")
    SECRET_KEY: str = os.getenv("SECRET_KEY")
    ALGORITHM: str = os.getenv("ALGORITHM", "HS256")
    ACCESS_TOKEN_EXPIRE_MINUTES: int = int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES", 60))

    model_config = SettingsConfigDict(env_file=".env", extra="allow")

# Instancia global de configuración accesible en toda la aplicación
settings = Settings()
