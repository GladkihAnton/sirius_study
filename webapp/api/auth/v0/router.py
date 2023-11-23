import time

from fastapi import APIRouter, Depends
from sqlalchemy import text
from sqlalchemy.ext.asyncio import AsyncSession

from webapp.db.postgres import async_session, async_db_connection

auth_router = APIRouter(prefix='/auth')

