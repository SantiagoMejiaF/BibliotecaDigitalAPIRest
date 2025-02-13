"""
Módulo de configuración de la base de datos.

Gestiona la conexión con SQLAlchemy y el ORM.

Autor: Santiago Mejía Fernández
Fecha: 13/02/2025
"""

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
from app.core.config import settings

DATABASE_URL = settings.DATABASE_URL

engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False} if "sqlite" in DATABASE_URL else {})
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

def get_db():
    """
    Dependencia para obtener una sesión de base de datos.

    Yields:
        Session: Sesión de SQLAlchemy para consultas.
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
