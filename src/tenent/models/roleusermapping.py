from sqlalchemy import Column, String, Boolean, DateTime, Integer, Index
from sqlalchemy.orm import DeclarativeBase
from sqlalchemy.sql import func
from datetime import datetime
from src.tenent.models.tenent import Tenent
from sqlalchemy import ForeignKey
from src.tenent.models.user import User
from src.tenent.models.role import Role


class RoleUserMappingBase(DeclarativeBase):
    pass

class RoleUserMapping(RoleUserMappingBase):

    __tablename__ = "role_user_mappings"

    id = Column(Integer, primary_key=True, autoincrement=True)
    tenent_id = Column(Integer, ForeignKey(Tenent.id))
    user_id = Column(Integer, ForeignKey(User.id))
    role_id = Column(Integer, ForeignKey(Role.id))
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    __table_args__ = (
        Index("idx_user_role", "user_id", "role_id"),
    )