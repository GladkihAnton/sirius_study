from fastapi import Depends, HTTPException, Body
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from starlette import status

from webapp.api.auth.v0.router import auth_router
from webapp.db.postgres import async_db_connection
from webapp.models.sirius.user import User
from webapp.schema.auth.v0.login import LoginQuery
from webapp.utils.auth.jwt import jwt_auth
from webapp.utils.auth.password import hash_password



@auth_router.post('/login')
async def login(
    body: LoginQuery = Depends(),
    db_session: AsyncSession = Depends(async_db_connection),
):
    query = select(User).where(
        User.email == body.email,
        User.hashed_password == hash_password(body.password),
    )
    user: User | None = (await db_session.execute(query)).scalar_one_or_none()
    print(user)
    access_token: str

    if user is None:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED)

    access_token = jwt_auth.create_token({'email': user.email})

    return {'ok': access_token}
