from typing import Any, Dict

from fastapi import Body, Depends, HTTPException
from redis import Redis
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from starlette import status

from webapp.api.auth.v0.router import auth_router
from webapp.db.postgres import async_db_connection
from webapp.db.redis_cache import get_redis
from webapp.integrations.auth.validator import validate_refresh_token, validate_token
from webapp.integrations.redis.key_builder import refresh_cache_key
from webapp.models.sirius.user import User
from webapp.schema.auth.v0.login import LoginQuery
from webapp.utils.auth.jwt import jwt_auth
from webapp.utils.auth.password import hash_password


@auth_router.post('/refresh')
async def login(
    token: Dict[str, Any] = Depends(validate_refresh_token),
    db_session: AsyncSession = Depends(async_db_connection),
    redis: Redis = Depends(get_redis),
):
    query = select(User).where(User.id == token['user_id'])
    user: User | None = (await db_session.execute(query)).scalar_one_or_none()

    if user is None:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED)

    access_token, refresh_token = await jwt_auth.create_pair_token(user, redis)

    return {
        'access_token': access_token,
        'refresh_token': refresh_token,
    }
