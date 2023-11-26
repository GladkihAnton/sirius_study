from sqlalchemy import Boolean, Column, Integer, String

from ..meta import SIRIUS_SCHEMA, Base


class User(Base):
    __tablename__ = 'user'
    __table_args__ = {'schema': SIRIUS_SCHEMA}

    id: int = Column(Integer, primary_key=True, index=True, unique=True)

    email: str = Column(String(length=320), unique=True, index=True, nullable=False)
    hashed_password: str = Column('password', String(128), nullable=False)

    code: str = Column(String(128), nullable=False)

    is_active: bool = Column(Boolean, default=True, nullable=False)
