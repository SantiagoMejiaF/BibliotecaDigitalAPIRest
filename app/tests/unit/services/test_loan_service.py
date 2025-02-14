import pytest
from unittest.mock import MagicMock
from app.services.loan_service import LoanService
from app.schemas.book import BookResponse
from app.models.book import Book


@pytest.fixture
def mock_db():
    """
    Mock para la sesión de la base de datos.
    """
    return MagicMock()


@pytest.fixture
def mock_book():
    """
    Mock para un libro.
    """
    return MagicMock(spec=Book, id=1, title="Cien años de soledad", borrowed_by_id=None)


def test_borrow_book_success(mock_db, mock_book):
    """
    Prueba que un usuario pueda tomar prestado un libro correctamente.
    """
    mock_db.query().filter().first.return_value = mock_book

    result = LoanService.borrow_book(mock_db, book_id=1, user_id=2)

    assert result is not None
    assert isinstance(result, BookResponse)
    assert result.borrowed_by_id == 2


def test_borrow_book_not_available(mock_db):
    """
    Prueba que no se pueda tomar prestado un libro ya prestado.
    """
    mock_book = MagicMock(spec=Book, id=1, title="Cien años de soledad", borrowed_by_id=3)
    mock_db.query().filter().first.return_value = mock_book

    result = LoanService.borrow_book(mock_db, book_id=1, user_id=2)

    assert result is None


def test_return_book_success(mock_db, mock_book):
    """
    Prueba que un usuario pueda devolver un libro correctamente.
    """
    mock_book.borrowed_by_id = 2
    mock_db.query().filter().first.return_value = mock_book

    result = LoanService.return_book(mock_db, book_id=1)

    assert result is not None
    assert isinstance(result, BookResponse)
    assert result.borrowed_by_id is None


def test_return_book_not_borrowed(mock_db):
    """
    Prueba que no se pueda devolver un libro que no estaba prestado.
    """
    mock_book = MagicMock(spec=Book, id=1, title="Cien años de soledad", borrowed_by_id=None)
    mock_db.query().filter().first.return_value = mock_book

    result = LoanService.return_book(mock_db, book_id=1)

    assert result is None
