"""
Настройки работы с БД.
"""
from typing import Optional
from uuid import uuid4

from asyncpg import Connection
from sqlalchemy import NullPool, QueuePool
from sqlalchemy.ext.asyncio import AsyncEngine, async_sessionmaker, create_async_engine

from conf.config import settings


class CConnection(Connection):
    def _get_unique_id(self, prefix: str) -> str:
        return f'__asyncpg_{prefix}_{uuid4()}__'


def create_engine() -> AsyncEngine:
    return create_async_engine(
        settings.DATABASE_URL,
        poolclass=QueuePool,
        connect_args={
            'connection_class': CConnection,
            'statement_cache_size': 0,
            # 'timeout': 2,
        },
        pool_size=5,
        max_overflow=10,
        pool_recycle=30,
    )


def create_session(engine: Optional[AsyncEngine] = None) -> 'async_sessionmaker':
    return async_sessionmaker(
        bind=engine or create_engine(),
        autocommit=False,
        autoflush=False,
        expire_on_commit=False,
    )


engine = create_engine()
async_session = create_session(engine)


async def async_db_connection():
    async with async_session() as session:
        yield session
