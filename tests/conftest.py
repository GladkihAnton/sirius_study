import pytest
from sqlalchemy import create_engine

from conf.config import settings
from webapp.models.meta import metadata


@pytest.fixture(scope='session')
def init_database():
    db_url = settings.DATABASE_URL
    db_url = db_url.replace('postgresql+asyncpg', 'postgresql')

    engine = create_engine(db_url)

    metadata.create_all(engine)
    yield
    metadata.drop_all(engine)
