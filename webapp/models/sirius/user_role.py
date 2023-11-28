from typing import List

from sqlalchemy import Column, Integer, ForeignKey

from ..meta import SIRIUS_SCHEMA, Base


class UserRole(Base):
    __tablename__ = 'user_role'
    __table_args__ = {'schema': SIRIUS_SCHEMA}

    id: int = Column(Integer, primary_key=True, index=True, unique=True)

    role_id: str = Column(Integer, ForeignKey(f'{SIRIUS_SCHEMA}.role.id'), nullable=False)
    user_id: str = Column(Integer, ForeignKey(f'{SIRIUS_SCHEMA}.user.id'), nullable=False)
