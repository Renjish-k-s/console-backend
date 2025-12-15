from sqlalchemy import Column, String, Boolean, DateTime, Integer, Index
from sqlalchemy.orm import DeclarativeBase
from sqlalchemy.sql import func
from datetime import datetime

class TenentBase(DeclarativeBase):
    pass

class Tenent(TenentBase):
    __tablename__ = "tenents"

    id = Column(Integer, primary_key=True, autoincrement=True)
    organization_name = Column(String(128), nullable=False, unique=True)
    is_active = Column(Boolean, nullable=False, default=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    __table_args__ = (
        Index("idx_name", "organization_name"),
    )