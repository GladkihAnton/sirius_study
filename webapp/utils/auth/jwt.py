from typing import Dict, Any

from fastapi import HTTPException
from jose import jwt, JWTError
from starlette import status

from conf.config import settings


class JwtAuth:
    def __init__(self, secret: str):
        self.secret = secret

    def create_token(self, user_data: Dict[str, Any]):
        return jwt.encode(user_data, self.secret)

    def decode_token(self, token: str):
        try:
            return jwt.decode(token, self.secret)
        except JWTError:
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN)


jwt_auth = JwtAuth(settings.JWT_SECRET_SALT)