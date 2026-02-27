from habit_tracker.config import settings
from redis import asyncio as aioredis

class RedisClient:
    def __init__(self, url: str, max_connections: int = 20):
        self._url = url
        self._max_connections = max_connections
        self._client: aioredis.Redis | None = None

    async def connect(self):
        if self._client is None:
            self._client = aioredis.from_url(
                self._url,
                encoding="utf-8",
                decode_responses=True,
                max_connections=self._max_connections,
            )
        return self._client

    async def get_client(self):
        if self._client is None:
            await self.connect()
        return self._client

    async def set(self, key: str, value: str, expire: int = None):
        client = await self.get_client()
        await client.set(key, value, ex=expire)

    async def get(self, key: str):
        client = await self.get_client()
        return await client.get(key)

    async def close(self):
        if self._client:
            await self._client.close()
            self._client = None


redis_client = RedisClient(settings.get_redis_url())
