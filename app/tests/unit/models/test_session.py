import pytest
from sqlalchemy.exc import IntegrityError
from app.core.database import SessionLocal
from app.models.session import SessionToken

def test_create_duplicate_session_token():
    """Prueba que la creación de un token duplicado falle por restricción de unicidad."""
    session = SessionLocal()
    try:
        token1 = SessionToken(user_id=100, token="abcdef123456")
        session.add(token1)
        session.commit()
    except IntegrityError:
        session.rollback()

    with pytest.raises(IntegrityError):
        token2 = SessionToken(user_id=2, token="abcdef123456")  # Token duplicado
        session.add(token2)
        session.commit()
    session.rollback()
    session.close()

def test_create_session_token_without_user():
    """Prueba que la creación de un token sin user_id falle."""
    session = SessionLocal()
    token = SessionToken(token="abcdef123456")
    session.add(token)
    with pytest.raises(IntegrityError):
        session.commit()
    session.rollback()
    session.close()
