from redis.asyncio import ConnectionPool, Redis

from conf.config import settings
from webapp.db import redis_cache


async def setup_redis() -> None:
    """
    Инициализация Redis.
    """
    pool = ConnectionPool(
        host=settings.REDIS_HOST,
        port=settings.REDIS_PORT,
        # password=settings.REDIS_PASSWORD,
        # db=settings.REDIS_DB,
        health_check_interval=10,
        socket_keepalive=True,
    )
    redis_cache.redis_cache = Redis(
        connection_pool=pool,
        # socket_timeout=settings.REDIS_SOCKET_TIMEOUT,
        # socket_connect_timeout=settings.REDIS_SOCKET_CONNECT_TIMEOUT,
    )
