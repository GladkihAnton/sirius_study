from typing import Annotated, Any, Dict

from fastapi import Depends, Header, HTTPException
from redis import Redis
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from starlette import status

from webapp.api.auth.v0.router import auth_router
from webapp.db.postgres import async_db_connection
from webapp.db.redis_cache import get_redis
from webapp.integrations.auth.validator import validate_token
from webapp.integrations.redis.key_builder import refresh_cache_key
from webapp.models.sirius.user import User
from webapp.utils.auth.jwt import jwt_auth
from webapp.utils.auth.password import hash_password


@auth_router.get('/info')
async def info(
    token: Dict[str, Any] = Depends(validate_token),
    redis: Redis = Depends(get_redis),
):
    print(await redis.get('access_token'))

    return {'ok': token}
