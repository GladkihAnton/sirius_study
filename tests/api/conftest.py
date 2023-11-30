import json
from pathlib import Path
from typing import List

import pytest_asyncio
from fastapi import FastAPI
from sqlalchemy import insert
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, AsyncSession

from conf.config import settings
from webapp.db.postgres import async_db_connection
from webapp.models.meta import metadata


@pytest_asyncio.fixture()
async def db_session() -> AsyncSession:
    engine = create_async_engine(settings.DATABASE_URL)
    connection = await engine.connect()
    transaction = await connection.begin()

    try:
        session_maker = async_sessionmaker(bind=connection, class_=AsyncSession, expire_on_commit=False)
        session = session_maker()

        # app.dependency_overrides[async_db_connection] = override_async_db_connection

        yield session

    finally:
        await transaction.rollback()
        await connection.close()
        await engine.dispose()

@pytest_asyncio.fixture()
async def load_fixture(
    fixtures: List[Path],
    db_session: AsyncSession,
) -> AsyncSession:
    for fixture in fixtures:
        table = metadata.tables[fixture.stem]

        with open(fixture, 'r') as f:
            data = json.load(f)

        query = insert(table).values(data)


        await db_session.execute(query)
        await db_session.commit()
