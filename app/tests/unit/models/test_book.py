import pytest
from sqlalchemy.exc import IntegrityError
from app.core.database import SessionLocal
from app.models.book import Book

def test_create_book():
    """Prueba la creación de un libro válido en la base de datos."""
    session = SessionLocal()
    book = Book(title="Cien años de soledad", publication_year=1967, author_id=1)
    session.add(book)
    session.commit()
    session.refresh(book)
    assert book.id is not None
    assert book.title == "Cien años de soledad"
    assert book.publication_year == 1967
    assert book.author_id == 1
    session.close()

def test_create_book_without_title():
    """Prueba que la creación de un libro sin título falle."""
    session = SessionLocal()
    book = Book(publication_year=1967, author_id=1)
    session.add(book)
    with pytest.raises(IntegrityError):
        session.commit()
    session.rollback()
    session.close()

def test_create_book_without_publication_year():
    """Prueba la creación de un libro sin año de publicación (opcional)."""
    session = SessionLocal()
    book = Book(title="El coronel no tiene quien le escriba", author_id=1)
    session.add(book)
    session.commit()
    session.refresh(book)
    assert book.id is not None
    assert book.title == "El coronel no tiene quien le escriba"
    assert book.publication_year is None
    session.close()

def test_delete_book():
    """Prueba la eliminación de un libro de la base de datos."""
    session = SessionLocal()
    book = Book(title="Crónica de una muerte anunciada", publication_year=1981, author_id=1)
    session.add(book)
    session.commit()
    session.refresh(book)
    book_id = book.id
    session.delete(book)
    session.commit()
    deleted_book = session.get(Book, book_id)
    assert deleted_book is None
    session.close()
