from datetime import timedelta

from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    DATABASE_URL: str
    JWT_SECRET_SALT: str

    REDIS_HOST: str
    REDIS_PORT: str
    REDIS_PREFIX: str = 'auth_sirius'

    ACCESS_TOKEN_LIFETIME: timedelta = timedelta(minutes=15)
    REFRESH_TOKEN_LIFETIME: timedelta = timedelta(hours=1)


settings = Settings()
