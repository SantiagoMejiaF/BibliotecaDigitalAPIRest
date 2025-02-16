import pytest
from sqlalchemy.exc import IntegrityError
from datetime import date
from app.core.database import SessionLocal
from app.models.author import Author

def test_create_author():
    """Prueba la creación de un autor válido en la base de datos."""
    session = SessionLocal()
    author = Author(name="Gabriel García Márquez", birth_date=date(1927, 3, 6))
    session.add(author)
    session.commit()
    session.refresh(author)
    assert author.id is not None
    assert author.name == "Gabriel García Márquez"
    assert author.birth_date == date(1927, 3, 6)
    session.close()

def test_create_author_without_name():
    """Prueba que la creación de un autor sin nombre falle."""
    session = SessionLocal()
    author = Author(birth_date=date(1927, 3, 6))
    session.add(author)
    with pytest.raises(IntegrityError):
        session.commit()
    session.rollback()
    session.close()

def test_create_author_without_birth_date():
    """Prueba la creación de un autor sin fecha de nacimiento (opcional)."""
    session = SessionLocal()
    author = Author(name="Isabel Allende")
    session.add(author)
    session.commit()
    session.refresh(author)
    assert author.id is not None
    assert author.name == "Isabel Allende"
    assert author.birth_date is None
    session.close()

def test_delete_author():
    """Prueba la eliminación de un autor y la cascada sobre sus libros."""
    session = SessionLocal()
    author = Author(name="Pablo Neruda")
    session.add(author)
    session.commit()
    session.refresh(author)
    author_id = author.id
    session.delete(author)
    session.commit()
    deleted_author = session.get(Author, author_id)
    assert deleted_author is None
    session.close()
