import pytest
from unittest.mock import patch
from app.api.routes.loans import router

@pytest.fixture
def test_client(client, mock_current_user):
    """
    Registra el router de préstamos en el cliente de pruebas con autenticación.
    """
    with patch("app.api.dependencies.get_current_user", return_value=mock_current_user):
        client.app.include_router(router)
        yield client

def test_borrow_book_success(test_client, mock_db, mock_loan_service):
    """
    Prueba que un usuario pueda tomar prestado un libro correctamente.
    """
    mock_loan_service.borrow_book.return_value = {
        "id": 1, "title": "Cien años de soledad", "borrowed_by_id": 2
    }

    with patch("app.services.loan_service.LoanService", mock_loan_service):
        response = test_client.post("/loans/borrow/1/2")
        assert response.status_code == 200
        assert response.json()["borrowed_by_id"] == 2

def test_borrow_book_not_available(test_client, mock_db, mock_loan_service):
    """
    Prueba que no se pueda tomar prestado un libro ya prestado.
    """
    mock_loan_service.borrow_book.return_value = None

    with patch("app.services.loan_service.LoanService", mock_loan_service):
        response = test_client.post("/loans/borrow/1/2")
        assert response.status_code == 400

def test_return_book_success(test_client, mock_db, mock_loan_service):
    """
    Prueba que un usuario pueda devolver un libro correctamente.
    """
    mock_loan_service.return_book.return_value = {
        "id": 1, "title": "Cien años de soledad", "borrowed_by_id": None
    }

    with patch("app.services.loan_service.LoanService", mock_loan_service):
        response = test_client.post("/loans/return/1")
        assert response.status_code == 200
        assert response.json()["borrowed_by_id"] is None
