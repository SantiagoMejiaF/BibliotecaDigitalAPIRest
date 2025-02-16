import pytest
from sqlalchemy.exc import IntegrityError
from app.core.database import SessionLocal
from app.models.role import Role

from app.models.user import User  # Asegúrate de importar el modelo de usuario

from app.models.user import User
from app.models.session import SessionToken

def test_create_role():
    """Prueba la creación de un rol válido en la base de datos."""
    session = SessionLocal()

    session.query(SessionToken).delete()
    session.commit()

    session.query(User).delete()
    session.commit()

    session.query(Role).delete()
    session.commit()

    role = Role(name="ADMINISTRADOR")
    session.add(role)
    session.commit()
    session.refresh(role)

    assert role.id is not None
    assert role.name == "ADMINISTRADOR"

    session.close()

def test_create_duplicate_role():
    """Prueba que la creación de un rol duplicado falle por restricción de unicidad."""
    session = SessionLocal()
    try:
        role1 = Role(name="USUARIO")
        session.add(role1)
        session.commit()
    except IntegrityError:
        session.rollback()

    with pytest.raises(IntegrityError):
        role2 = Role(name="USUARIO")
        session.add(role2)
        session.commit()
    session.rollback()
    session.close()


def test_create_role_without_name():
    """Prueba que la creación de un rol sin nombre falle."""
    session = SessionLocal()
    role = Role()
    session.add(role)
    with pytest.raises(IntegrityError):
        session.commit()
    session.rollback()
    session.close()


def test_delete_role():
    """Prueba la eliminación de un rol de la base de datos."""
    session = SessionLocal()
    role = Role(name="MODERADOR")
    session.add(role)
    session.commit()
    session.refresh(role)
    role_id = role.id
    session.delete(role)
    session.commit()
    deleted_role = session.get(Role, role_id)
    assert deleted_role is None
    session.close()
