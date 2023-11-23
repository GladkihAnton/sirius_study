from typing import Annotated

from fastapi import Depends, HTTPException, Header
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from starlette import status

from webapp.api.auth.v0.router import auth_router
from webapp.db.postgres import async_db_connection
from webapp.models.sirius.user import User
from webapp.utils.auth.jwt import jwt_auth
from webapp.utils.auth.password import hash_password



@auth_router.get('/info')
async def info(
    authorization: Annotated[str | None, Header()] = None,
):
    access_token = jwt_auth.decode_token(authorization.split()[0])

    return {'ok': access_token}
