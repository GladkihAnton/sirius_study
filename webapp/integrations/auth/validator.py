from typing import Annotated

from fastapi import Depends, Header, HTTPException
from redis.asyncio import Redis
from starlette import status

from webapp.db.redis_cache import get_redis
from webapp.integrations.redis.key_builder import refresh_cache_key
from webapp.utils.auth.jwt import jwt_auth


def validate_token(authorization: Annotated[str | None, Header()] = None):
    return jwt_auth.decode_token(authorization.split()[1])


def validate_access_token(authorization: Annotated[str | None, Header()] = None):
    token = jwt_auth.decode_token(authorization.split()[1])
    if token['type'] != jwt_auth.ACCESS_TOKEN_T:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN)

    return token


async def validate_refresh_token(
    authorization: Annotated[str | None, Header()] = None,
    redis: Redis = Depends(get_redis),
):
    token = authorization.split()[1]
    parsed_token = jwt_auth.decode_token(token)
    if parsed_token['type'] != jwt_auth.REFRESH_TOKEN_T:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN)

    if parsed_token['type'] != jwt_auth.REFRESH_TOKEN_T:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN)

    cache_key = refresh_cache_key(parsed_token['user_id'])
    if (await redis.get(cache_key)).decode() != token:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN)

    return parsed_token
