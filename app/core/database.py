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

# Configuración del motor SQLAlchemy para PostgreSQL
engine = create_engine(DATABASE_URL, pool_pre_ping=True)

# Crear una sesión de base de datos
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Base para los modelos ORM
Base = declarative_base()

def init_db():
    """
    Inicializa la base de datos creando las tablas si no existen y agregando roles.
    """
    from app.models.role import Role

    print("🔄 Verificando y creando tablas en la base de datos...")
    Base.metadata.create_all(bind=engine)

    # Insertar roles si no existen
    db = SessionLocal()
    if not db.query(Role).filter(Role.name == "ADMINISTRADOR").first():
        db.add(Role(name="ADMINISTRADOR"))
    if not db.query(Role).filter(Role.name == "USUARIO").first():
        db.add(Role(name="USUARIO"))
    db.commit()
    db.close()


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
