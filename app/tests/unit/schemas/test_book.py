import pytest
from pydantic import ValidationError

from app.schemas import BookResponse


def test_book_response_valid():
    """Prueba la creación de un BookResponse válido."""
    data = {
        "id": 1,
        "title": "1984",
        "publication_year": 1949,
        "author_id": 2,
        "borrowed_by_id": 3
    }
    book = BookResponse(**data)
    assert book.id == data["id"]
    assert book.title == data["title"]
    assert book.publication_year == data["publication_year"]
    assert book.author_id == data["author_id"]
    assert book.borrowed_by_id == data["borrowed_by_id"]

def test_book_response_missing_publication_year():
    """Prueba la creación de un BookResponse sin el año de publicación (opcional)."""
    data = {
        "id": 1,
        "title": "Fahrenheit 451",
        "author_id": 2,
        "borrowed_by_id": None
    }
    book = BookResponse(**data)
    assert book.publication_year is None

def test_book_response_missing_borrowed_by_id():
    """Prueba la creación de un BookResponse sin el usuario que lo ha tomado prestado (opcional)."""
    data = {
        "id": 1,
        "title": "Brave New World",
        "publication_year": 1932,
        "author_id": 2
    }
    book = BookResponse(**data)
    assert book.borrowed_by_id is None

def test_book_response_invalid_id():
    """Prueba que la validación falle si el id no es un número entero."""
    data = {
        "id": "uno",
        "title": "The Catcher in the Rye",
        "publication_year": 1951,
        "author_id": 2,
        "borrowed_by_id": None
    }
    with pytest.raises(ValidationError):
        BookResponse(**data)

def test_book_response_missing_title():
    """Prueba que la validación falle si falta el título del libro."""
    data = {
        "id": 1,
        "publication_year": 2000,
        "author_id": 2,
        "borrowed_by_id": None
    }
    with pytest.raises(ValidationError):
        BookResponse(**data)
