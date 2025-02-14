import pytest
from unittest.mock import MagicMock
from app.services.author_service import AuthorService
from app.schemas.author import AuthorCreate, AuthorResponse
from app.models.author import Author


@pytest.fixture
def mock_db():
    """Mock para la sesión de base de datos."""
    return MagicMock()


@pytest.fixture
def mock_author():
    """Mock para un autor de prueba."""
    return Author(id=1, name="Gabriel García Márquez")


def test_create_author_success(mock_db, mock_author):
    """
    ✅ Prueba que un autor se cree correctamente en la base de datos.
    """
    mock_db.add.return_value = None
    mock_db.commit.return_value = None
    mock_db.refresh.side_effect = lambda author: setattr(author, "id", 1)  # Asigna un ID al autor

    author_data = AuthorCreate(name="Gabriel García Márquez")
    result = AuthorService.create_author(mock_db, author_data)

    assert isinstance(result, AuthorResponse)
    assert result.id == 1
    assert result.name == "Gabriel García Márquez"


def test_get_author_by_id_success(mock_db, mock_author):
    """
    Prueba que se obtenga un autor por su ID correctamente.
    """
    mock_db.query().filter().first.return_value = mock_author

    result = AuthorService.get_author_by_id(mock_db, 1)

    assert isinstance(result, AuthorResponse)
    assert result.id == 1
    assert result.name == "Gabriel García Márquez"


def test_get_author_by_id_not_found(mock_db):
    """
    Prueba que devuelve `None` si el autor no existe en la base de datos.
    """
    mock_db.query().filter().first.return_value = None

    result = AuthorService.get_author_by_id(mock_db, 99)

    assert result is None


def test_get_all_authors_success(mock_db, mock_author):
    """
    Prueba que se obtengan todos los autores de la base de datos.
    """
    mock_db.query().all.return_value = [mock_author]

    result = AuthorService.get_all_authors(mock_db)

    assert isinstance(result, list)
    assert len(result) == 1
    assert result[0].id == 1
    assert result[0].name == "Gabriel García Márquez"


def test_update_author_success(mock_db, mock_author):
    """
    Prueba que un autor se actualiza correctamente en la base de datos.
    """
    mock_db.query().filter().first.return_value = mock_author

    author_data = AuthorCreate(name="Isabel Allende")
    result = AuthorService.update_author(mock_db, 1, author_data)

    assert isinstance(result, AuthorResponse)
    assert result.id == 1
    assert result.name == "Isabel Allende"


def test_update_author_not_found(mock_db):
    """
    Prueba que devuelve `None` si el autor a actualizar no existe.
    """
    mock_db.query().filter().first.return_value = None

    author_data = AuthorCreate(name="Isabel Allende")
    result = AuthorService.update_author(mock_db, 99, author_data)

    assert result is None


def test_delete_author_success(mock_db, mock_author):
    """
    Prueba que un autor se elimine correctamente de la base de datos.
    """
    mock_db.query().filter().first.return_value = mock_author

    result = AuthorService.delete_author(mock_db, 1)

    assert result is True


def test_delete_author_not_found(mock_db):
    """
    Prueba que devuelve `False` si el autor a eliminar no existe.
    """
    mock_db.query().filter().first.return_value = None

    result = AuthorService.delete_author(mock_db, 99)

    assert result is False
