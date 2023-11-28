from typing import TYPE_CHECKING

from sqlalchemy import Column, ForeignKey, Integer
from sqlalchemy.orm import Mapped, relationship

from ..meta import SIRIUS_SCHEMA, Base

if TYPE_CHECKING:
    from webapp.models.sirius.path import Path


class RolePath(Base):
    __tablename__ = 'role_path'
    __table_args__ = {'schema': SIRIUS_SCHEMA}

    id: int = Column(Integer, primary_key=True, index=True, unique=True)

    role_id: Mapped[int] = Column(Integer, ForeignKey(f'{SIRIUS_SCHEMA}.role.id'), nullable=False)
    path_id: Mapped[int] = Column(Integer, ForeignKey(f'{SIRIUS_SCHEMA}.path.id'), nullable=False)

    path: Mapped['Path'] = relationship(
        'Path',
        back_populates='role_paths',
        uselist=False,
    )
