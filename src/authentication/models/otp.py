from sqlalchemy import Column, String, Boolean, DateTime, Integer, Index
from sqlalchemy.orm import DeclarativeBase
from sqlalchemy.sql import func
from datetime import datetime

class OTPBase(DeclarativeBase):
    pass

class OTP(OTPBase):
    __tablename__ = "otp"

    id = Column(Integer, primary_key=True, autoincrement=True)
    email = Column(String(128), nullable=False, index=True)
    otp = Column(String(6), nullable=False)   # typical length
    is_used = Column(Boolean, nullable=False, default=False)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    __table_args__ = (
        Index("idx_email_otp", "email", "otp"),
    )
