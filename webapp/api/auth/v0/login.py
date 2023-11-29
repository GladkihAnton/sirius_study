from fastapi import Body, Depends, HTTPException
from redis import Redis
from sqlalchemy import select, and_
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload, joinedload
from starlette import status

from webapp.utils.deps_latency import time_it
from webapp.api.auth.v0.router import auth_router
from webapp.db.postgres import async_db_connection
from webapp.db.redis_cache import get_redis
from webapp.integrations.redis.key_builder import refresh_cache_key
from webapp.models.sirius.role import Role
from webapp.models.sirius.user import User
from webapp.models.sirius.user_role import UserRole
from webapp.schema.auth.v0.login import LoginQuery
from webapp.utils.auth.jwt import jwt_auth
from webapp.utils.auth.password import hash_password


@auth_router.get('/login')
async def login(
    body: LoginQuery = Depends(),
    db_session: AsyncSession = Depends(async_db_connection),
    redis: Redis = Depends(get_redis),
):
    user = await _get_user(body, db_session)

    if user is None:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED)

    access_token, refresh_token = await jwt_auth.create_pair_token(user, redis)

    return {
        'access_token': access_token,
        'refresh_token': refresh_token,
    }


@time_it
async def _get_user(body, db_session):
    query = (
        select(User)
        .where(
            User.email == body.email,
            User.hashed_password == hash_password(body.password),
        )
        .options(selectinload(User.roles))
    )
    return (await db_session.execute(query)).scalar_one_or_none()
