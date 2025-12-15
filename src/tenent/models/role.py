from sqlalchemy import Column, String, Boolean, DateTime, Integer, Index
from sqlalchemy.orm import DeclarativeBase
from sqlalchemy.sql import func
from datetime import datetime
from src.tenent.models.tenent import Tenent
from sqlalchemy import ForeignKey

class RoleBase(DeclarativeBase):
    pass

class Role(RoleBase):
    __tablename__ = "roles"

    id = Column(Integer, primary_key=True, autoincrement=True)
    tenent_id = Column(Integer, ForeignKey(Tenent.id))
    role_name = Column(String(50), nullable=False)
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    __table_args__ = (
        Index("idx_role_name", "role_name"),
    )

    