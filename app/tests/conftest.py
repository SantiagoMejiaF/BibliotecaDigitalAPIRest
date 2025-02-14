from app.services.author_service import AuthorService
from app.services.book_service import BookService
from app.services.loan_service import LoanService
from app.services.session_service import SessionService
import pytest
from unittest.mock import MagicMock, patch
from fastapi.testclient import TestClient
from app.main import app
from app.services.user_service import UserService
from sqlalchemy.orm import Session

@pytest.fixture
def client():
    """
    Cliente de pruebas para FastAPI.
    Proporciona un cliente de prueba sin autenticación.
    """
    return TestClient(app)

@pytest.fixture
def mock_author_service():
    """
    Mock para el servicio de autores.
    """
    return MagicMock(spec=AuthorService)

@pytest.fixture
def mock_book_service():
    """
    Mock para el servicio de libros.
    """
    return MagicMock(spec=BookService)

@pytest.fixture
def mock_loan_service():
    """
    Mock para el servicio de préstamos de libros.
    """
    return MagicMock(spec=LoanService)

@pytest.fixture
def mock_session_service():
    """
    Mock para el servicio de sesiones.
    """
    return MagicMock(spec=SessionService)

@pytest.fixture
def test_client():
    """ Cliente de pruebas para FastAPI """
    return TestClient(app)


@pytest.fixture
def mock_db():
    """ Mock de la sesión de la base de datos """
    return MagicMock(spec=Session)


@pytest.fixture
def mock_user_service():
    """ Mock del servicio de usuarios """
    mock_service = MagicMock(spec=UserService)
    return mock_service


@pytest.fixture
def mock_admin_user():
    """ Usuario ADMINISTRADOR simulado """
    return {"id": 99, "name": "Admin", "email": "admin@mail.com", "role": "ADMINISTRADOR"}


@pytest.fixture
def mock_current_user():
    """ Usuario USUARIO simulado """
    return {"id": 2, "name": "Test User", "email": "test@mail.com", "role": "USUARIO"}


@pytest.fixture(autouse=True)
def disable_authentication():
    """ 🔧 Simula la autenticación sin necesidad de token """
    with patch("app.api.dependencies.get_current_user", return_value={"id": 99, "role": "ADMINISTRADOR"}):
        yield
