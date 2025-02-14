import pytest
from unittest.mock import MagicMock, patch
from app.services.session_service import SessionService
from app.models.session import SessionToken


@pytest.fixture
def mock_db():
    """
    Crea un mock de la sesión de base de datos.
    """
    return MagicMock()


@pytest.fixture
def mock_session_token():
    """
    Mock de un token de sesión generado.
    """
    return SessionToken(user_id=1, token="mocked_token")


def test_create_session_success(mock_db, mock_session_token):
    """
    Prueba que se cree un nuevo token de sesión correctamente.
    """
    mock_db.query().filter().delete.return_value = None  # Simula eliminación previa
    mock_db.add.return_value = None
    mock_db.commit.return_value = None
    mock_db.refresh.side_effect = lambda x: setattr(x, "token", "mocked_token")

    with patch("app.core.security.generate_token", return_value="mocked_token"):
        result = SessionService.create_session(mock_db, 1)

    assert isinstance(result, SessionToken)
    assert result.token == "mocked_token"
    assert result.user_id == 1


def test_get_session_found(mock_db, mock_session_token):
    """
    Prueba que se obtenga una sesión existente por su token.
    """
    mock_db.query().filter().first.return_value = mock_session_token

    result = SessionService.get_session(mock_db, "mocked_token")

    assert result is not None
    assert isinstance(result, SessionToken)
    assert result.token == "mocked_token"
    assert result.user_id == 1


def test_get_session_not_found(mock_db):
    """
    Prueba que si el token no existe, devuelve `None`.
    """
    mock_db.query().filter().first.return_value = None

    result = SessionService.get_session(mock_db, "invalid_token")

    assert result is None


def test_delete_session_success(mock_db):
    """
    Prueba que se elimine un token de sesión correctamente.
    """
    mock_db.query().filter().delete.return_value = 1  # Simula que se eliminó un token
    mock_db.commit.return_value = None

    result = SessionService.delete_session(mock_db, "mocked_token")

    assert result is None  # La función no retorna nada, solo ejecuta la eliminación


def test_delete_session_not_found(mock_db):
    """
    Prueba que si el token no existe, la eliminación no genere error.
    """
    mock_db.query().filter().delete.return_value = 0  # Simula que no se encontró el token
    mock_db.commit.return_value = None

    result = SessionService.delete_session(mock_db, "invalid_token")

    assert result is None  # No hay retorno, pero no debe lanzar error
