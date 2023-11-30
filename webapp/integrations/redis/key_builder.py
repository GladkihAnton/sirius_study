from datetime import datetime

from conf.config import settings
from webapp.models.sirius.user import User


def refresh_cache_key(user_id: int) -> str:
    return f'{settings.REDIS_PREFIX}:refresh_token:{user_id}'


def user_rps_cache_key(user_id: int) -> str:
    return f'{settings.REDIS_PREFIX}:user_rps:{user_id}:{str(datetime.utcnow())[:-7]}'
