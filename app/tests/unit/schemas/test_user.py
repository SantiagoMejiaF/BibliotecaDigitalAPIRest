import pytest
from pydantic import ValidationError
from datetime import datetime

from app.schemas import UserResponse


def test_user_response_valid():
    """Prueba la creación de un UserResponse válido."""
    data = {
        "id": 1,
        "name": "Juan Pérez",
        "email": "juan.perez@example.com",
        "registered_at": datetime.utcnow()
    }
    user = UserResponse(**data)
    assert user.id == data["id"]
    assert user.name == data["name"]
    assert user.email == data["email"]
    assert isinstance(user.registered_at, datetime)

def test_user_response_missing_name():
    """Prueba que la validación falle si falta el campo name."""
    data = {
        "id": 1,
        "email": "juan.perez@example.com",
        "registered_at": datetime.utcnow()
    }
    with pytest.raises(ValidationError):
        UserResponse(**data)

def test_user_response_invalid_email():
    """Prueba que la validación falle si el email no es válido."""
    data = {
        "id": 1,
        "name": "Juan Pérez",
        "email": "correo-no-valido",
        "registered_at": datetime.utcnow()
    }
    with pytest.raises(ValidationError):
        UserResponse(**data)

def test_user_response_missing_registered_at():
    """Prueba que la validación falle si falta el campo registered_at."""
    data = {
        "id": 1,
        "name": "Juan Pérez",
        "email": "juan.perez@example.com"
    }
    with pytest.raises(ValidationError):
        UserResponse(**data)

def test_user_response_invalid_registered_at():
    """Prueba que la validación falle si registered_at no es un datetime válido."""
    data = {
        "id": 1,
        "name": "Juan Pérez",
        "email": "juan.perez@example.com",
        "registered_at": "fecha-invalida"
    }
    with pytest.raises(ValidationError):
        UserResponse(**data)
