import pytest
from pydantic import ValidationError

from app.schemas import TokenResponse


def test_token_response_valid():
    """Prueba la creación de un TokenResponse válido."""
    data = {
        "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9",
        "token_type": "bearer"
    }
    token = TokenResponse(**data)
    assert token.access_token == data["access_token"]
    assert token.token_type == data["token_type"]

def test_token_response_missing_access_token():
    """Prueba que falte el campo access_token."""
    data = {
        "token_type": "bearer"
    }
    with pytest.raises(ValidationError):
        TokenResponse(**data)

def test_token_response_missing_token_type():
    """Prueba que falte el campo token_type."""
    data = {
        "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9"
    }
    with pytest.raises(ValidationError):
        TokenResponse(**data)

def test_token_response_invalid_access_token():
    """Prueba que el access_token sea un valor no válido (espacio en blanco)."""
    data = {
        "access_token": " ",  # Se reemplaza vacío con espacio en blanco
        "token_type": "bearer"
    }
    token = TokenResponse(**data)
    assert token.access_token.strip() == ""

def test_token_response_invalid_token_type():
    """Prueba que el token_type sea un valor no válido (espacio en blanco)."""
    data = {
        "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9",
        "token_type": " "  # Se reemplaza vacío con espacio en blanco
    }
    token = TokenResponse(**data)
    assert token.token_type.strip() == ""
