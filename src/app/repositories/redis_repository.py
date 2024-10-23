from typing import Optional

from redis.asyncio import Redis

from app.repositories.abc_repository import TokenRepository


class RedisTokenRepository(TokenRepository):

    def __init__(self, redis_url: str):
        self.redis = Redis.from_url(redis_url, auto_close_connection_pool=True)

    async def init(self):
        self.redis = Redis.from_url(self.redis_url)

    async def set_token(self, username: str, token: str) -> None:
        await self.redis.set(f"token:{username}", token)

    async def get_token(self, username: str) -> Optional[str]:
        return await self.redis.get(f"token:{username}")
