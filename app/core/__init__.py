"""
Módulo de inicialización del core de la aplicación.

Este archivo permite la importación centralizada de los módulos de configuración y seguridad.

Autor: Santiago Mejía Fernández
Fecha: 13/02/2025
"""

from app.core.config import settings
from app.core.database import Base, engine, get_db
