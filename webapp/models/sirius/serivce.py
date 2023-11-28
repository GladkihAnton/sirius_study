from typing import List, TYPE_CHECKING

from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import Mapped, relationship

from ..meta import SIRIUS_SCHEMA, Base

if TYPE_CHECKING:
    from webapp.models.sirius.path import Path


class Service(Base):
    __tablename__ = 'service'
    __table_args__ = {'schema': SIRIUS_SCHEMA}

    id: int = Column(Integer, primary_key=True, index=True, unique=True)

    name: str = Column(String(length=320), unique=True, index=True, nullable=False)
    url: str = Column(String(length=320), nullable=False)

    paths: Mapped[List['Path']] = relationship(
        'Path',
        back_populates='service',
    )