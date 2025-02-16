import pytest
from sqlalchemy.exc import IntegrityError
from app.core.database import SessionLocal
from app.models.user import User
from app.models.role import Role

def test_create_duplicate_user_email():
    """Prueba que la creación de un usuario con un correo duplicado falle."""
    session = SessionLocal()
    try:
        user1 = User(name="Ana López", email="ana.lopez@example.com", password="securepassword", role_id=1)
        session.add(user1)
        session.commit()
    except IntegrityError:
        session.rollback()

    with pytest.raises(IntegrityError):
        user2 = User(name="Pedro Gómez", email="ana.lopez@example.com", password="anotherpassword", role_id=2)
        session.add(user2)
        session.commit()
    session.rollback()
    session.close()

def test_create_user_without_email():
    """Prueba que la creación de un usuario sin correo falle."""
    session = SessionLocal()
    if not session.query(Role).filter_by(name="USUARIO").first():
        role = Role(name="USUARIO")
        session.add(role)
        session.commit()

    user = User(name="Carlos Sánchez", password="mypassword", role_id=1)
    session.add(user)
    with pytest.raises(IntegrityError):
        session.commit()
    session.rollback()
    session.close()
