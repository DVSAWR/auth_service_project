import pytest
from unittest.mock import AsyncMock
from app.service import AuthService
from app.models import User


@pytest.fixture
def mock_user_repository():
    return AsyncMock()


@pytest.fixture
def mock_token_repository():
    return AsyncMock()


@pytest.fixture
def auth_service(mock_user_repository, mock_token_repository):
    return AuthService(
        user_repository=mock_user_repository,
        token_repository=mock_token_repository,
        secret_key="secret_key",
        algorithm="HS256",
    )


@pytest.mark.asyncio
async def test_registration_success(
    auth_service, mock_user_repository, mock_token_repository
):
    # ARRANGE
    username = "user123"
    password = "Password123!"
    email = "user@example.com"
    mock_user_repository.get_user_by_username.return_value = None
    mock_user_repository.get_user_by_email.return_value = None
    mock_user_repository.create_user.return_value = None
    mock_token_repository.set_token.return_value = None

    # ACT
    token = await auth_service.registration(username, password, email)

    # ASSERT
    assert token is not None
    assert mock_user_repository.create_user.called
    assert mock_token_repository.set_token.called


@pytest.mark.asyncio
async def test_registration_user_exists(auth_service, mock_user_repository):
    # ARRANGE
    username = "user123"
    password = "Password123!"
    email = "user@example.com"
    mock_user_repository.get_user_by_username.return_value = User(
        username=username, password_hash="qwe", email=email
    )

    # ACT
    token = await auth_service.registration(username, password, email)

    # ASSERT
    assert token is None
    assert not mock_user_repository.create_user.called


@pytest.mark.asyncio
async def test_authorization_success(
    auth_service, mock_user_repository, mock_token_repository
):
    # ARRANGE
    username = "user123"
    password = "Password123!"
    user = User(
        username=username,
        password_hash=auth_service._hash_password(password),
        email="user@example.com",
    )
    mock_user_repository.get_user_by_username.return_value = user
    mock_token_repository.get_token.return_value = None
    mock_token_repository.set_token.return_value = None  # Simulate token storage

    # ACT
    token = await auth_service.authorization(username, password)

    # ASSERT
    assert token is not None
    assert mock_token_repository.get_token.called
    assert mock_token_repository.set_token.called


@pytest.mark.asyncio
async def test_authorization_incorrect_password(auth_service, mock_user_repository):
    # ARRANGE
    username = "user123"
    password = "WrongPassword!"
    user = User(
        username=username,
        password_hash=auth_service._hash_password("Password123!"),
        email="user@example.com",
    )
    mock_user_repository.get_user_by_username.return_value = user

    # ACT
    token = await auth_service.authorization(username, password)

    # ASSERT
    assert token is None


@pytest.mark.asyncio
async def test_authorization_user_not_found(auth_service, mock_user_repository):
    # ARRANGE
    username = "user123"
    password = "Password123!"
    mock_user_repository.get_user_by_username.return_value = None  # User does not exist

    # ACT
    token = await auth_service.authorization(username, password)

    # ASSERT
    assert token is None
