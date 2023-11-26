from fastapi import Depends, Request
from fastapi.responses import JSONResponse, ORJSONResponse
from redis.asyncio import Redis
from sqlalchemy.ext.asyncio import AsyncSession

from webapp.api.proxy.router import proxy_router
from webapp.db.postgres import async_db_connection
from webapp.db.redis_cache import get_redis


@proxy_router.api_route('/{service:str}/{path:path}', methods=['GET', 'HEAD', 'POST', 'PUT', 'DELETE', 'PATCH'])
async def reverse_proxy(
    request: Request,
    service: str,
    path: str,
    redis: Redis = Depends(get_redis),
    db: AsyncSession = Depends(async_db_connection),
) -> ORJSONResponse:
    return ORJSONResponse({})
