from typing import List, TYPE_CHECKING

from sqlalchemy import Boolean, Column, ForeignKey, Integer, String
from sqlalchemy.orm import relationship, Mapped

from ..meta import SIRIUS_SCHEMA, Base

if TYPE_CHECKING:
    from webapp.models.sirius.serivce import Service
    from webapp.models.sirius.role_path import RolePath


class Path(Base):
    __tablename__ = 'path'
    __table_args__ = {'schema': SIRIUS_SCHEMA}

    id: int = Column(Integer, primary_key=True, index=True, unique=True)

    name: str = Column(String(length=320), nullable=False)
    path: str = Column(String(length=320), nullable=False)

    service_id: str = Column(Integer, ForeignKey(f'{SIRIUS_SCHEMA}.service.id'), nullable=False)
    # service: str = relationship('Service', uselist=False)

    is_active: bool = Column(Boolean, default=True, nullable=False)

    type: bool = Column(String(128), default=True, nullable=False)


    role_paths: Mapped[List['RolePath']] = relationship(
        'RolePath',
        back_populates='path',
    )

    service: Mapped['Service'] = relationship(
        'Service',
        back_populates='paths',
        uselist=False,
    )