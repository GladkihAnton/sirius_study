from redis import Redis


redis_cache: Redis


async def get_redis() -> Redis:
    """Return the Redis instance."""
    return redis_cache
