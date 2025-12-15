from sqlalchemy import Column, String, Boolean, DateTime, Integer, Index
from sqlalchemy.orm import DeclarativeBase
from sqlalchemy.sql import func
from datetime import datetime
from src.tenent.models.tenent import Tenent
from sqlalchemy import ForeignKey


class UserBase(DeclarativeBase):
    pass

class User(UserBase):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, autoincrement=True)
    tenent_id = Column(Integer,ForeignKey(Tenent.id))
    username = Column(String(50), nullable=False, unique=True)
    email = Column(String(128), nullable=False, unique=True)
    hashed_password = Column(String(256), nullable=False)
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    __table_args__ = (
        Index("idx_username", "username"),
        Index("idx_email", "email"),
    )

