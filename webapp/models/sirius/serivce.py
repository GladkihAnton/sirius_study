from sqlalchemy import Boolean, Column, Integer, String

from ..meta import SIRIUS_SCHEMA, Base


class Service(Base):
    __tablename__ = 'service'
    __table_args__ = {'schema': SIRIUS_SCHEMA}

    id: int = Column(Integer, primary_key=True, index=True, unique=True)

    name: str = Column(String(length=320), unique=True, index=True, nullable=False)
    url: str = Column(String(length=320), nullable=False)
