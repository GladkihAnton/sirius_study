from collections import defaultdict
from typing import Dict, Any, List, Optional

from fastapi import Depends, Request, HTTPException
from fastapi.responses import JSONResponse, ORJSONResponse
from redis.asyncio import Redis
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import joinedload
from starlette import status

from webapp.api.proxy.router import proxy_router
from webapp.db.postgres import async_db_connection
from webapp.db.redis_cache import get_redis
from webapp.integrations.auth.validator import validate_access_token
from webapp.integrations.proxy.request import do_proxy_request
from webapp.integrations.redis.rate_limitter import validate_rps
from webapp.models.sirius.path import Path
from webapp.models.sirius.role_path import RolePath


@proxy_router.api_route('/{service:str}/{path:path}', methods=['GET', 'HEAD', 'POST', 'PUT', 'DELETE', 'PATCH'])
async def reverse_proxy(
    request: Request,
    service: str,
    path: str,
    redis: Redis = Depends(get_redis),
    db: AsyncSession = Depends(async_db_connection),
    token: Dict[str, Any] = Depends(validate_access_token),
) -> ORJSONResponse:
    query = (
        select(RolePath)
        .where(RolePath.role_id.in_(token['role_ids']))
        .options(
            joinedload(RolePath.path).joinedload(Path.service)
        )
    )
    role_paths: List[RolePath] = (await db.scalars(query)).all()


    service_to_paths: Dict[str, Dict[str, List[str]]] = defaultdict(lambda: defaultdict(list))
    for role_path in role_paths:
        service_to_paths[role_path.path.service.name]['paths'].append(role_path.path.path)
        service_to_paths[role_path.path.service.name]['url'] = role_path.path.service.url

    if service not in service_to_paths:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN)

    is_valid_path = False
    for saved_path in service_to_paths[service]['paths']:
        if saved_path.startswith(path):
            is_valid_path = True
            break

    if not is_valid_path:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN)

    await validate_rps(token['user_id'], redis, 1)

    url = service_to_paths[service]['url']
    # await do_proxy_request(request, f'{url}/{path}')

    return ORJSONResponse({})
