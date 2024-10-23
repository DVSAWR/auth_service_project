from typing import Optional

from sqlalchemy.exc import IntegrityError
from sqlalchemy.future import select

from ..database import AsyncSessionLocal
from ..models import User
from .abc_repository import UserRepository


class PostgresUserRepository(UserRepository):
    async def create_user(self, user: User) -> User:
        async with AsyncSessionLocal() as session:
            session.add(user)
            try:
                await session.commit()
                await session.refresh(user)
                return user
            except IntegrityError:
                await session.rollback()
                raise ValueError("User with this username or email already exists.")

    async def get_user_by_username(self, username: str) -> Optional[User]:
        async with AsyncSessionLocal() as session:
            query = select(User).where(User.username == username)
            result = await session.execute(query)
            return result.scalar_one_or_none()

    async def get_user_by_email(self, email: str) -> Optional[User]:
        async with AsyncSessionLocal() as session:
            query = select(User).where(User.email == email)
            result = await session.execute(query)
            return result.scalar_one_or_none()
