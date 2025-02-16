import pytest
from pydantic import ValidationError

from app.schemas.role import RoleResponse, RoleEnum


def test_role_response_valid():
    """Prueba la creación de un RoleResponse válido."""
    data = {
        "id": 1,
        "name": "ADMINISTRADOR"
    }
    role = RoleResponse(**data)
    assert role.id == data["id"]
    assert role.name == RoleEnum.ADMINISTRADOR

def test_role_response_invalid_id():
    """Prueba que la validación falle si el id no es un número entero."""
    data = {
        "id": "uno",
        "name": "ADMINISTRADOR"
    }
    with pytest.raises(ValidationError):
        RoleResponse(**data)

def test_role_response_invalid_name():
    """Prueba que la validación falle si el nombre no es un valor permitido en RoleEnum."""
    data = {
        "id": 1,
        "name": "SUPER_ADMIN"
    }
    with pytest.raises(ValidationError):
        RoleResponse(**data)

def test_role_response_missing_id():
    """Prueba que la validación falle si falta el campo id."""
    data = {
        "name": "ADMINISTRADOR"
    }
    with pytest.raises(ValidationError):
        RoleResponse(**data)

def test_role_response_missing_name():
    """Prueba que la validación falle si falta el campo name."""
    data = {
        "id": 1
    }
    with pytest.raises(ValidationError):
        RoleResponse(**data)
