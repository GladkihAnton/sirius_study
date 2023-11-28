from typing import TYPE_CHECKING, List

from sqlalchemy import Boolean, Column, Integer, String
from sqlalchemy.orm import relationship, Mapped

from ..meta import SIRIUS_SCHEMA, Base

if TYPE_CHECKING:
    from webapp.models.sirius.role import Role


class User(Base):
    __tablename__ = 'user'
    __table_args__ = {'schema': SIRIUS_SCHEMA}

    id: int = Column(Integer, primary_key=True, index=True, unique=True)

    email: str = Column(String(length=320), unique=True, index=True, nullable=False)
    hashed_password: str = Column('password', String(128), nullable=False)

    code: str = Column(String(128), nullable=False)

    is_active: bool = Column(Boolean, default=True, nullable=False)
    roles: Mapped[List['Role']] = relationship(
        'Role',
        secondary=f'{SIRIUS_SCHEMA}.user_role',
        back_populates='users',
    )
