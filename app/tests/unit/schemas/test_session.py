import pytest
from pydantic import ValidationError
from datetime import datetime

from app.schemas import SessionTokenResponse


def test_session_token_response_valid():
    """Prueba la creación de un SessionTokenResponse válido."""
    data = {
        "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9",
        "token_type": "bearer",
        "created_at": datetime.utcnow()
    }
    token = SessionTokenResponse(**data)
    assert token.access_token == data["access_token"]
    assert token.token_type == data["token_type"]
    assert isinstance(token.created_at, datetime)

def test_session_token_response_missing_access_token():
    """Prueba que la validación falle si falta el access_token."""
    data = {
        "token_type": "bearer",
        "created_at": datetime.utcnow()
    }
    with pytest.raises(ValidationError):
        SessionTokenResponse(**data)

def test_session_token_response_missing_created_at():
    """Prueba que la validación falle si falta el campo created_at."""
    data = {
        "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9",
        "token_type": "bearer"
    }
    with pytest.raises(ValidationError):
        SessionTokenResponse(**data)

def test_session_token_response_invalid_created_at():
    """Prueba que la validación falle si created_at no es un datetime válido."""
    data = {
        "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9",
        "token_type": "bearer",
        "created_at": "fecha-invalida"
    }
    with pytest.raises(ValidationError):
        SessionTokenResponse(**data)
