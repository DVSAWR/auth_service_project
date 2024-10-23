from abc import ABC, abstractmethod
from typing import Optional

from ..models import User


# ABC REPOSITORIES
class UserRepository(ABC):
    """Abstract repository for user."""

    @abstractmethod
    async def create_user(self, user: User) -> User:
        """Create a new user in the repository."""
        pass

    @abstractmethod
    async def get_user_by_username(self, username: str) -> Optional[User]:
        """Get user by username."""
        pass

    @abstractmethod
    async def get_user_by_email(self, email: str) -> Optional[User]:
        """Get user by email."""
        pass


class TokenRepository(ABC):
    """Abstract repository for token."""

    @abstractmethod
    async def set_token(self, username: str, token: str) -> None:
        """Create a token for user."""
        pass

    @abstractmethod
    async def get_token(self, username: str) -> Optional[str]:
        """Get token associated with the user, or return None if not found."""
        pass
