from fastapi import HTTPException
from redis.asyncio import Redis
from starlette import status

from webapp.integrations.redis.key_builder import user_rps_cache_key


async def validate_rps(user_id: int, redis: Redis, rps: int):
    cache_key = user_rps_cache_key(user_id)
    current_rps= await redis.incrby(cache_key)
    await redis.expire(cache_key, 3)

    if current_rps > rps:
        raise HTTPException(status.HTTP_429_TOO_MANY_REQUESTS)
