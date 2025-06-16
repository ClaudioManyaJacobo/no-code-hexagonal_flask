import pytest
from unittest.mock import MagicMock
import sys
import os
from werkzeug.security import generate_password_hash

# Agrega la ruta para poder importar desde application
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from application.user.user_service import UserService

# Clase mock para simular un usuario sin que pytest lo interprete como test
class MockUser:
    def __init__(self, user_id, name, email, password):
        self.user_id = user_id
        self.name = name
        self.email = email
        self.password = password  

def test_authenticate_user_success():
    # Arrange
    mock_repo = MagicMock()
    raw_password = "Password123!"
    hashed_password = generate_password_hash(raw_password)
    mock_user = MockUser(
        user_id=17,
        name="marie",
        email="amamama@gmail.com",
        password=hashed_password
    )
    mock_repo.get_user_by_email.return_value = mock_user
    service = UserService(mock_repo)
    # Act
    result = service.authenticate_user("amamama@gmail.com", raw_password)
    # Assert
    assert result == mock_user

def test_authenticate_user_wrong_password():
    # Arrange
    mock_repo = MagicMock()
    correct_password = "Password123!"
    hashed_password = generate_password_hash(correct_password)

    mock_user = MockUser(
        user_id=1,
        name="TestUser",
        email="test@gmail.com",
        password=hashed_password
    )
    mock_repo.get_user_by_email.return_value = mock_user
    service = UserService(mock_repo)
    # Act
    result = service.authenticate_user("test@gmail.com", "Hashpassword111120202!")
    # Assert
    assert result is None

def test_authenticate_user_no_user():
    # Arrange
    mock_repo = MagicMock()
    mock_repo.get_user_by_email.return_value = None
    service = UserService(mock_repo)
    # Act
    result = service.authenticate_user("nonexistent@gmail.com", "TestPassword0112!")
    # Assert
    assert result is None
