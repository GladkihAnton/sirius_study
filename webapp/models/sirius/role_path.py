from sqlalchemy import Boolean, Column, ForeignKey, Integer, String

from ..meta import SIRIUS_SCHEMA, Base


class RolePath(Base):
    __tablename__ = 'role_path'
    __table_args__ = {'schema': SIRIUS_SCHEMA}

    id: int = Column(Integer, primary_key=True, index=True, unique=True)

    role_id: str = Column(ForeignKey(f'{SIRIUS_SCHEMA}.role.id'), nullable=False)
    path_id: str = Column(ForeignKey(f'{SIRIUS_SCHEMA}.path.id'), nullable=False)
