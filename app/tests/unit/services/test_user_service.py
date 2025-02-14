import pytest
from unittest.mock import MagicMock, patch
from datetime import datetime
from app.services.user_service import UserService
from app.models.user import User
from app.models.role import Role
from app.models.session import SessionToken
from app.schemas.user import UserCreate, UserResponse
from app.core.security import hash_password, generate_token


@pytest.fixture
def mock_db():
    """Mock para la sesión de la base de datos."""
    return MagicMock()


@pytest.fixture
def mock_user():
    """Mock para un usuario existente."""
    return User(
        id=1,
        name="Santiago Mejía",
        email="test@mail.com",
        password=hash_password("securepassword"),
        role_id=2,
        registered_at=datetime.utcnow()
    )


@pytest.fixture
def mock_role():
    """Mock para el rol de usuario."""
    return Role(id=2, name="USUARIO")


@pytest.fixture
def mock_token():
    """Mock para un token de sesión activo."""
    return SessionToken(user_id=1, token="mocked_token", created_at=datetime.utcnow())


def test_create_user_success(mock_db, mock_role):
    """Prueba que un usuario se crea correctamente con el rol USUARIO."""

    mock_db.query().filter().first.return_value = mock_role
    mock_db.add.return_value = None

    mock_user_created = User(
        id=2,
        name="Test User",
        email="testuser@mail.com",
        password=hash_password("securepassword"),
        role_id=2,
        registered_at=datetime.utcnow()
    )
    mock_db.refresh.side_effect = lambda obj: obj.__dict__.update(mock_user_created.__dict__)

    user_data = UserCreate(name="Test User", email="testuser@mail.com", password="securepassword")
    result = UserService.create_user(mock_db, user_data)

    assert isinstance(result, UserResponse)
    assert result.name == "Test User"
    assert result.email == "testuser@mail.com"
    assert result.id == 2
    assert isinstance(result.registered_at, datetime)


def test_get_user_by_id_found(mock_db, mock_user):
    """Prueba que se obtiene un usuario por ID correctamente."""

    mock_db.query().filter().first.return_value = mock_user

    result = UserService.get_user_by_id(mock_db, 1)

    assert isinstance(result, UserResponse)
    assert result.id == 1
    assert result.name == "Santiago Mejía"
    assert result.email == "test@mail.com"


def test_get_user_by_id_not_found(mock_db):
    """Prueba que se retorna None cuando el usuario no existe."""

    mock_db.query().filter().first.return_value = None

    result = UserService.get_user_by_id(mock_db, 99)

    assert result is None


def test_get_user_by_email_found(mock_db, mock_user):
    """Prueba que se obtiene un usuario por correo correctamente."""

    mock_db.query().filter().first.return_value = mock_user

    result = UserService.get_user_by_email(mock_db, "test@mail.com")

    assert isinstance(result, User)
    assert result.email == "test@mail.com"


def test_get_user_by_email_not_found(mock_db):
    """Prueba que se retorna None cuando el usuario no existe."""

    mock_db.query().filter().first.return_value = None

    result = UserService.get_user_by_email(mock_db, "notfound@mail.com")

    assert result is None


def test_get_all_users(mock_db, mock_user):
    """Prueba que se obtiene una lista de usuarios."""

    mock_db.query().all.return_value = [mock_user]

    result = UserService.get_all_users(mock_db)

    assert isinstance(result, list)
    assert len(result) == 1
    assert isinstance(result[0], UserResponse)


def test_update_user_success(mock_db, mock_user):
    """Prueba que un usuario se actualiza correctamente."""

    mock_db.query().filter().first.return_value = mock_user

    updated_data = UserCreate(name="Nuevo Nombre", email="new@mail.com", password="newpassword")

    updated_user = mock_user
    updated_user.name = updated_data.name
    updated_user.email = updated_data.email
    updated_user.password = hash_password(updated_data.password)

    mock_db.refresh.side_effect = lambda obj: obj.__dict__.update(updated_user.__dict__)

    result = UserService.update_user(mock_db, 1, updated_data)

    assert isinstance(result, UserResponse)
    assert result.name == "Nuevo Nombre"
    assert result.email == "new@mail.com"


def test_update_user_not_found(mock_db):
    """Prueba que no se actualiza un usuario si no existe."""

    mock_db.query().filter().first.return_value = None

    updated_data = UserCreate(name="Nuevo Nombre", email="new@mail.com", password="newpassword")
    result = UserService.update_user(mock_db, 99, updated_data)

    assert result is None


def test_delete_user_success(mock_db, mock_user):
    """Prueba que un usuario se elimina correctamente."""

    mock_db.query().filter().first.return_value = mock_user

    result = UserService.delete_user(mock_db, 1)

    assert result is True


def test_delete_user_not_found(mock_db):
    """Prueba que no se elimina un usuario si no existe."""

    mock_db.query().filter().first.return_value = None

    result = UserService.delete_user(mock_db, 99)

    assert result is False


def test_authenticate_user_invalid_password(mock_db, mock_user):
    """Prueba que un usuario con contraseña incorrecta no recibe token."""

    mock_db.query().filter().first.return_value = mock_user

    result = UserService.authenticate_user(mock_db, "test@mail.com", "wrongpassword")

    assert result is None


def test_authenticate_user_not_found(mock_db):
    """Prueba que un usuario inexistente no recibe token."""

    mock_db.query().filter().first.return_value = None

    result = UserService.authenticate_user(mock_db, "notfound@mail.com", "securepassword")

    assert result is None


def test_logout_user_success(mock_db, mock_user):
    """Prueba que un usuario cierra sesión correctamente eliminando su token."""

    mock_db.query().filter().first.return_value = mock_user

    mock_db.query().filter().delete.return_value = 1

    result = UserService.logout_user(mock_db, 1)

    assert result is True


def test_logout_user_not_found(mock_db):
    """Prueba que si no hay sesión activa, no se elimina token."""

    mock_db.query().filter().first.return_value = None

    mock_db.query().filter().delete.return_value = 0

    result = UserService.logout_user(mock_db, 99)

    assert result is False
