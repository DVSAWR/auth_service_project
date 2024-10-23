from pydantic import BaseModel
from sqlalchemy import BigInteger, Boolean, Column, String
from sqlalchemy.orm import declarative_base

Base = declarative_base()


class User(Base):
    """User model representing the user in the system."""

    __tablename__ = "users"

    id = Column(BigInteger, primary_key=True, autoincrement=True)
    username = Column(String(64), nullable=False, unique=True)
    password_hash = Column(String(256), nullable=False)
    email = Column(String(256), nullable=False, unique=True)
    verify_status = Column(Boolean, default=False, nullable=False)


# REQUEST / RESPONSE MODELS
class UserRequest(BaseModel):
    username: str
    password: str
    email: str


class UserDataResponse(BaseModel):
    user_id: int
    username: str
    email: str
    token: str


class TokenResponse(BaseModel):
    access_token: str
    token_type: str
