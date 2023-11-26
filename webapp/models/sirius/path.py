from sqlalchemy import Boolean, Column, ForeignKey, Integer, String
from sqlalchemy.orm import relationship

from ..meta import SIRIUS_SCHEMA, Base


class Path(Base):
    __tablename__ = 'path'
    __table_args__ = {'schema': SIRIUS_SCHEMA}

    id: int = Column(Integer, primary_key=True, index=True, unique=True)

    name: str = Column(String(length=320), nullable=False)
    path: str = Column(String(length=320), nullable=False)

    service_id: str = Column(ForeignKey(f'{SIRIUS_SCHEMA}.service.id'), nullable=False)
    # service: str = relationship('Service', uselist=False)

    is_active: bool = Column(Boolean, default=True, nullable=False)

    type: bool = Column(String(128), default=True, nullable=False)
