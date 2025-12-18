# src/authentication/models/invalid_token.py
from sqlalchemy import Column, String, DateTime
from sqlalchemy.sql import func
from sqlalchemy.orm import DeclarativeBase

class InvalidTokenBase(DeclarativeBase):
    pass

class InvalidToken(InvalidTokenBase):
    __tablename__ = "invalid_tokens"

    jti = Column(String, primary_key=True, index=True)
    expires_at = Column(DateTime, nullable=False)
    created_at = Column(DateTime, server_default=func.now())
