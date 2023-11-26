import uuid
from datetime import datetime, timedelta
from typing import Any, Dict, Tuple

from fastapi import HTTPException
from jose import JWTError, jwt
from redis import Redis
from starlette import status

from conf.config import settings
from webapp.integrations.redis.key_builder import refresh_cache_key
from webapp.models.sirius.user import User


class JwtAuth:
    ACCESS_TOKEN_T = 'access_token'
    REFRESH_TOKEN_T = 'refresh_token'

    def __init__(self, secret: str):
        self.secret = secret

    async def create_pair_token(self, user: User, redis: Redis) -> Tuple[str, str]:
        access_token_id = uuid.uuid4().hex
        refresh_token_id = uuid.uuid4().hex

        now = datetime.utcnow()

        common_data = {
            'code': user.code,
            'user_id': user.id,
        }

        access_data = {
            'token_id': access_token_id,
            'type': self.ACCESS_TOKEN_T,
            'paired_id': refresh_token_id,
            'exp': now + settings.ACCESS_TOKEN_LIFETIME,
            **common_data,
        }
        access_token = jwt.encode(access_data, self.secret)

        refresh_exp = now + settings.REFRESH_TOKEN_LIFETIME
        refresh_data = {
            'token_id': refresh_token_id,
            'paired_id': access_token_id,
            'type': self.REFRESH_TOKEN_T,
            'exp': refresh_exp,
            **common_data,
        }

        refresh_token = jwt.encode(refresh_data, self.secret)
        await redis.set(refresh_cache_key(user.id), refresh_token, settings.REFRESH_TOKEN_LIFETIME)

        return access_token, refresh_token

    def decode_token(self, token: str):
        try:
            return jwt.decode(token, self.secret)
        except JWTError:
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN)


jwt_auth = JwtAuth(settings.JWT_SECRET_SALT)
