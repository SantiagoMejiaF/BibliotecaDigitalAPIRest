import pytest
from pydantic import ValidationError
from datetime import date

from app.schemas import AuthorResponse


def test_author_response_valid():
    """Prueba la creación de un AuthorResponse válido."""
    data = {
        "id": 1,
        "name": "Gabriel García Márquez",
        "birth_date": "1927-03-06"
    }
    author = AuthorResponse(**data)
    assert author.id == data["id"]
    assert author.name == data["name"]
    assert author.birth_date == date.fromisoformat(data["birth_date"])

def test_author_response_missing_birth_date():
    """Prueba la creación de un AuthorResponse sin la fecha de nacimiento (opcional)."""
    data = {
        "id": 2,
        "name": "Julio Cortázar"
    }
    author = AuthorResponse(**data)
    assert author.birth_date is None

def test_author_response_invalid_id():
    """Prueba que la validación falle si el id no es un número entero."""
    data = {
        "id": "uno",
        "name": "Isabel Allende",
        "birth_date": "1942-08-02"
    }
    with pytest.raises(ValidationError):
        AuthorResponse(**data)

def test_author_response_missing_name():
    """Prueba que la validación falle si falta el nombre del autor."""
    data = {
        "id": 3,
        "birth_date": "1975-05-23"
    }
    with pytest.raises(ValidationError):
        AuthorResponse(**data)

def test_author_response_invalid_birth_date():
    """Prueba que la validación falle si la fecha de nacimiento no es válida."""
    data = {
        "id": 4,
        "name": "Pablo Neruda",
        "birth_date": "fecha-invalida"
    }
    with pytest.raises(ValidationError):
        AuthorResponse(**data)
