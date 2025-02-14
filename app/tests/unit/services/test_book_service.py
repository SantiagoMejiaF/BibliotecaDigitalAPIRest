import pytest
from unittest.mock import MagicMock
from app.services.book_service import BookService
from app.models.book import Book
from app.models.author import Author
from app.schemas.book import BookCreate, BookResponse


@pytest.fixture
def mock_db():
    """
    Crea un mock de la sesión de base de datos.
    """
    return MagicMock()


@pytest.fixture
def mock_book():
    """
    Mock de un libro en la base de datos.
    """
    return Book(id=1, title="Cien años de soledad", author_id=1, publication_year=1967)


@pytest.fixture
def mock_author():
    """
    Mock de un autor en la base de datos.
    """
    return Author(id=1, name="Gabriel García Márquez")


def test_create_book_success(mock_db):
    """
    Prueba que se cree un nuevo libro correctamente.
    """
    mock_book = Book(id=1, title="Cien años de soledad", author_id=1, publication_year=1967)

    mock_db.add.return_value = None
    mock_db.commit.return_value = None
    mock_db.refresh.side_effect = lambda book: setattr(book, "id", 1)  # Asigna un id

    book_data = BookCreate(title="Cien años de soledad", author_id=1, publication_year=1967)
    result = BookService.create_book(mock_db, book_data)

    assert isinstance(result, BookResponse)
    assert result.id == 1
    assert result.title == "Cien años de soledad"
    assert result.author_id == 1


def test_get_book_by_id_found(mock_db, mock_book):
    """
    Prueba que se obtenga un libro existente por su ID.
    """
    mock_db.query().filter().first.return_value = mock_book

    result = BookService.get_book_by_id(mock_db, 1)

    assert result is not None
    assert isinstance(result, BookResponse)
    assert result.id == 1
    assert result.title == "Cien años de soledad"


def test_get_book_by_id_not_found(mock_db):
    """
    Prueba que si el libro no existe, devuelve `None`.
    """
    mock_db.query().filter().first.return_value = None

    result = BookService.get_book_by_id(mock_db, 99)

    assert result is None


def test_get_all_books(mock_db, mock_book):
    """
    Prueba que se obtenga la lista de todos los libros registrados.
    """
    mock_db.query().all.return_value = [mock_book]

    result = BookService.get_all_books(mock_db)

    assert isinstance(result, list)
    assert len(result) == 1
    assert isinstance(result[0], BookResponse)
    assert result[0].title == "Cien años de soledad"


def test_update_book_success(mock_db, mock_book):
    """
    Prueba que se actualicen los datos de un libro correctamente.
    """
    mock_db.query().filter().first.return_value = mock_book
    mock_db.commit.return_value = None
    mock_db.refresh.return_value = mock_book

    updated_data = BookCreate(title="Rayuela", author_id=1, publication_year=1963)
    result = BookService.update_book(mock_db, 1, updated_data)

    assert isinstance(result, BookResponse)
    assert result.title == "Rayuela"
    assert result.publication_year == 1963


def test_update_book_not_found(mock_db):
    """
    Prueba que si el libro no existe, devuelve `None` al intentar actualizarlo.
    """
    mock_db.query().filter().first.return_value = None

    updated_data = BookCreate(title="Rayuela", author_id=1, publication_year=1963)
    result = BookService.update_book(mock_db, 99, updated_data)

    assert result is None


def test_delete_book_success(mock_db, mock_book):
    """
    Prueba que se elimine un libro correctamente.
    """
    mock_db.query().filter().first.return_value = mock_book
    mock_db.delete.return_value = None
    mock_db.commit.return_value = None

    result = BookService.delete_book(mock_db, 1)

    assert result is True


def test_delete_book_not_found(mock_db):
    """
    Prueba que si el libro no existe, la eliminación devuelva `False`.
    """
    mock_db.query().filter().first.return_value = None

    result = BookService.delete_book(mock_db, 99)

    assert result is False


def test_search_books_by_title(mock_db, mock_book):
    """
    Prueba la búsqueda de libros por título.
    """
    mock_db.query().join().filter().all.return_value = [mock_book]

    result = BookService.search_books(mock_db, title="Cien años de soledad")

    assert isinstance(result, list)
    assert len(result) == 1
    assert result[0].title == "Cien años de soledad"


def test_search_books_by_author(mock_db, mock_book, mock_author):
    """
    Prueba la búsqueda de libros por autor.
    """
    mock_db.query().join().filter().all.return_value = [mock_book]

    result = BookService.search_books(mock_db, author="Gabriel García Márquez")

    assert isinstance(result, list)
    assert len(result) == 1
    assert result[0].author_id == 1


def test_search_books_by_year(mock_db, mock_book):
    """
    Prueba la búsqueda de libros por año de publicación.
    """
    mock_db.query().join().filter().all.return_value = [mock_book]

    result = BookService.search_books(mock_db, year=1967)

    assert isinstance(result, list)
    assert len(result) == 1
    assert result[0].publication_year == 1967


def test_search_books_not_found(mock_db):
    """
    Prueba que si no se encuentran libros, la búsqueda devuelve una lista vacía.
    """
    mock_db.query().join().filter().all.return_value = []

    result = BookService.search_books(mock_db, title="Libro no existente")

    assert isinstance(result, list)
    assert len(result) == 0
