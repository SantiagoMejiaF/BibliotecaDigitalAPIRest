import pytest
from unittest.mock import patch, MagicMock
from fastapi.testclient import TestClient
from app.api.routes.users import router
from app.services.user_service import UserService
from app.main import app
from datetime import datetime
from unittest.mock import patch
from app.schemas.user import UserResponse

# 📌 Registrar el router en la app para pruebas
app.include_router(router)


@pytest.fixture
def test_client():
    """Cliente de pruebas de FastAPI."""
    return TestClient(app)


@pytest.fixture
def mock_db():
    """Mock para la sesión de base de datos."""
    return MagicMock()


@pytest.fixture
def mock_user_service():
    """Mock para el servicio de usuario."""
    return MagicMock(spec=UserService)


@pytest.fixture
def mock_admin_user():
    """Mock para un usuario con rol ADMINISTRADOR."""
    return {"id": 99, "name": "Admin", "email": "admin@mail.com", "role": "ADMINISTRADOR"}  # Evita `id=1`


def test_create_user_success(test_client, mock_db, mock_user_service, mock_admin_user):
    """Prueba que se pueda crear un usuario sin violar restricciones de unicidad."""
    user_data = {"name": "Nuevo Usuario", "email": "nuevo@mail.com", "password": "securepassword"}

    mock_user_service.create_user.return_value = UserResponse(
        id=100,
        name="Nuevo Usuario",
        email="nuevo@mail.com",
        registered_at=datetime.utcnow()
    )

    with patch("app.api.dependencies.get_current_user", return_value=mock_admin_user):
        with patch("app.services.user_service.UserService.create_user", mock_user_service.create_user):
            response = test_client.post("/users/", json=user_data)

    assert response.status_code == 201
    assert response.json()["name"] == "Nuevo Usuario"
    assert response.json()["email"] == "nuevo@mail.com"
    assert "registered_at" in response.json()
