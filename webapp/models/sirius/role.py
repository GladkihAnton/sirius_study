from typing import List, TYPE_CHECKING

from sqlalchemy import Boolean, Column, Integer, String
from sqlalchemy.orm import relationship, Mapped

from ..meta import SIRIUS_SCHEMA, Base

if TYPE_CHECKING:
    from webapp.models.sirius.user import User


class Role(Base):
    __tablename__ = 'role'
    __table_args__ = {'schema': SIRIUS_SCHEMA}

    id: int = Column(Integer, primary_key=True, index=True, unique=True)

    name: str = Column(String(length=320), unique=True, index=True, nullable=False)

    users: Mapped[List['User']] = relationship(
        'User',
        secondary=f'{SIRIUS_SCHEMA}.user_role',
        back_populates='roles',
    )