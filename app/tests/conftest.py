import pytest
from unittest.mock import MagicMock, patch
from fastapi.testclient import TestClient
from sqlalchemy.orm import Session
from app.main import app
from app.services.user_service import UserService
from app.services.author_service import AuthorService
from app.services.book_service import BookService
from app.services.loan_service import LoanService
from app.services.session_service import SessionService
from app.api.dependencies import get_current_user, require_admin, require_user_or_admin
from app.schemas.user import UserResponse
from datetime import datetime


@pytest.fixture
def client():
    return TestClient(app)


@pytest.fixture
def mock_db():
    return MagicMock(spec=Session)


@pytest.fixture
def mock_user_service(monkeypatch):
    mock_service = MagicMock(spec=UserService)
    monkeypatch.setattr(UserService, "get_user_by_id", mock_service.get_user_by_id)
    monkeypatch.setattr(UserService, "get_all_users", mock_service.get_all_users)
    monkeypatch.setattr(UserService, "update_user", mock_service.update_user)
    monkeypatch.setattr(UserService, "delete_user", mock_service.delete_user)
    return mock_service


@pytest.fixture
def mock_author_service():
    return MagicMock(spec=AuthorService)


@pytest.fixture
def mock_book_service():
    return MagicMock(spec=BookService)


@pytest.fixture
def mock_loan_service():
    return MagicMock(spec=LoanService)


@pytest.fixture
def mock_session_service():
    return MagicMock(spec=SessionService)


@pytest.fixture
def mock_admin_user():
    return {"id": 99, "name": "Admin", "email": "admin@mail.com", "role": "ADMINISTRADOR"}


@pytest.fixture
def mock_current_user():
    return {"id": 2, "name": "Test User", "email": "test@mail.com", "role": "USUARIO"}


@pytest.fixture(autouse=True)
def mock_authentication(monkeypatch):
    def mock_get_current_user():
        return UserResponse(
            id=1,
            username="testuser",
            email="test@example.com",
            role="USUARIO",
            name="Test User",
            registered_at=str(datetime.utcnow())
        )

    monkeypatch.setattr("app.api.dependencies.get_current_user", mock_get_current_user)
    monkeypatch.setattr("app.api.dependencies.require_admin", lambda: None)
    monkeypatch.setattr("app.api.dependencies.require_user_or_admin", lambda: None)
