import jwt
from fastapi import Depends, FastAPI, Form, HTTPException, status
from fastapi.responses import RedirectResponse
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm

from app.config import config
from app.models import TokenResponse, UserDataResponse
from app.repositories.postgres_repository import PostgresUserRepository
from app.repositories.redis_repository import RedisTokenRepository
from app.service import AuthService


# FAST API
app = FastAPI()


# REPOSITORY PICK
user_repository = PostgresUserRepository()
token_repository = RedisTokenRepository(redis_url=config.REDIS_URL)

auth_service = AuthService(
    user_repository=user_repository,
    token_repository=token_repository,
    secret_key=config.SECRET_KEY,
    algorithm=config.ALGORITHM,
)


# REDIRECT ROOT TO /docs
@app.get("/")
async def redirect_to_docs():
    """Redirect from root to /docs."""
    return RedirectResponse(url="/docs")


# URLs
@app.post("/registration", response_model=TokenResponse)
async def registration(
    username: str = Form(...), password: str = Form(...), email: str = Form(...)
):
    """Registration new user in system."""
    token = await auth_service.registration(
        username=username,
        password=password,
        email=email,
    )

    if token is None:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid username or password or email.",
        )

    return TokenResponse(access_token=token, token_type="bearer")


@app.post("/authorization", response_model=TokenResponse)
async def authorization(user: OAuth2PasswordRequestForm = Depends()):
    """Authorization user in system."""
    token = await auth_service.authorization(
        username=user.username,
        password=user.password,
    )

    if token is None:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Wrong username or password.",
        )

    return TokenResponse(access_token=token, token_type="bearer")


@app.get("/user_data", response_model=UserDataResponse)
async def get_user_data(
    token: str = Depends(OAuth2PasswordBearer(tokenUrl="authorization")),
):
    """Returns the currently authenticated user's data along with the token."""

    try:
        payload = jwt.decode(token, config.SECRET_KEY, algorithms=[config.ALGORITHM])

        username = payload.get("username")

        if not username:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid token details.",
            )

        user = await user_repository.get_user_by_username(username)
        if user:
            token_value = await token_repository.get_token(username)
            return UserDataResponse(
                user_id=user.id,
                username=user.username,
                email=user.email,
                token=token_value,
            )

        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found.",
        )

    except jwt.ExpiredSignatureError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Token has expired.",
        )

    except jwt.InvalidTokenError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid token.",
        )
