import re
from datetime import datetime, timedelta
from typing import Optional

import bcrypt
import jwt

from .config import config
from .logconfig import custom_log
from .models import User
from .repositories.abc_repository import TokenRepository, UserRepository


class AuthService:
    """Service for registration and authorization."""

    def __init__(
        self,
        user_repository: UserRepository,
        token_repository: TokenRepository,
        secret_key: str,
        algorithm: str,
    ) -> None:
        self.user_repository = user_repository
        self.token_repository = token_repository
        self.secret_key = secret_key
        self.algorithm = algorithm

    async def registration(
        self, username: str, password: str, email: str
    ) -> Optional[str]:
        """Registration new user in system."""
        custom_log(
            f"~ Attempting registration with username: {username}, email: {email}"
        )

        if not all([username, password, email]):
            custom_log("~ Username, password, or email is missing.")
            return None

        if not self._is_valid_username(username):
            custom_log("~ Invalid username.")
            return None

        if not self._is_valid_email(email):
            custom_log("~ Invalid email.")
            return None

        existing_user_by_username = await self.user_repository.get_user_by_username(
            username
        )
        existing_user_by_email = await self.user_repository.get_user_by_email(email)

        if existing_user_by_username or existing_user_by_email:
            custom_log("~ User with provided username or email already exists.")
            return None

        hashed_password = self._hash_password(password)
        user = User(username=username, password_hash=hashed_password, email=email)
        await self.user_repository.create_user(user)

        token = self._create_jwt_token(user.id, user.username)
        await self.token_repository.set_token(user.username, token)

        custom_log(f"~ Successfully created token: {token}")
        return token

    async def authorization(self, username: str, password: str) -> Optional[str]:
        """Authorization user in system."""
        if not username or not password:
            return None

        user = await self.user_repository.get_user_by_username(username)

        if user is None or not self._check_password(password, user.password_hash):
            return None

        token = await self.token_repository.get_token(user.username)
        if token is not None and self._check_jwt_token(token, user.id, user.username):
            return token

        token = self._create_jwt_token(user.id, user.username)
        await self.token_repository.set_token(user.username, token)
        return token

    def _is_valid_username(self, username: str) -> bool:
        """Validate username.
        A valid username must be between 3 and 30 characters long and consist
        only of alphanumeric characters (A-z, 0-9).
        """
        return (3 <= len(username) <= 30) and bool(re.match("^[a-zA-Z0-9]+$", username))

    def _is_valid_email(self, email: str) -> bool:
        """Validate the format of an email address."""
        regex = r"^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$"
        return bool(re.match(regex, email))

    def _hash_password(self, password: str) -> str:
        """Hash a password using bcrypt."""
        return bcrypt.hashpw(password.encode(), bcrypt.gensalt()).decode()

    def _check_password(self, password: str, hashed_password: str) -> bool:
        """Verify a password against a hashed password."""
        return bcrypt.checkpw(password.encode(), hashed_password.encode())

    def _create_jwt_token(self, user_id: int, username: str) -> str:
        """Create a JWT token for the user."""
        expiration_time = datetime.now() + timedelta(
            minutes=config.JWT_EXPIRATION_MINUTES
        )
        return jwt.encode(
            payload={
                "user_id": user_id,
                "username": username,
                "exp": int(expiration_time.timestamp()),
            },
            key=self.secret_key,
            algorithm=self.algorithm,
        )

    def _check_jwt_token(self, token: str, user_id: int, username: str) -> bool:
        """Validate a JWT token and its associated user information."""
        try:
            payload = jwt.decode(token, self.secret_key, algorithms=[self.algorithm])
            if payload.get("exp") < int(datetime.now().timestamp()):
                return False
            return user_id == payload.get("user_id") and username == payload.get(
                "username"
            )
        except jwt.ExpiredSignatureError:
            return False
        except jwt.InvalidTokenError:
            return False
