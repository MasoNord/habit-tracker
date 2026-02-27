from redis import asyncio as aioredis
from habit_tracker.extensions.redis import redis_client

async def get_redis() -> aioredis.Redis:
    return await redis_client.get_client()