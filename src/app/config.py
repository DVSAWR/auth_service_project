import os

from dotenv import load_dotenv

load_dotenv(dotenv_path=os.path.join(os.path.dirname(__file__), "../.env"))


class Config:
    JWT_EXPIRATION_MINUTES: int = int(os.getenv("JWT_EXPIRATION_MINUTES", 1))
    ALGORITHM: str = os.getenv("ALGORITHM", "HS256")
    SECRET_KEY: str | None = os.getenv("SECRET_KEY")
    POSTGRES_URL: str | None = os.getenv("POSTGRES_URL")
    REDIS_URL: str | None = os.getenv("REDIS_URL")


config = Config()
