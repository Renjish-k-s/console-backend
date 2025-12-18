from typing import Dict
from datetime import datetime, timedelta, timezone
from typing import Optional
from jose import JWTError, jwt
from passlib.context import CryptContext
from fastapi import Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from src.database import get_db
from src.tenent.models.user import User
from src import config
from fastapi.security import OAuth2PasswordBearer

ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 1440
REFRESH_TOKEN_EXPIRE_DAYS = 7
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="auth/login")


pwd_context = CryptContext(
    schemes=["bcrypt"],
    deprecated="auto"
)


def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)

async def authenticate_user(db: AsyncSession, username: str, password: str) -> bool | User:
    result = await db.execute(select(User).filter(User.email == username))
    user = result.scalars().first()
    if not user:
        return False
    if not verify_password(password, user.hashed_password):
        return False
    return user


def create_access_token(data: Dict[str, str], expires_delta: Optional[timedelta] = None) -> str:
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.now(tz=timezone.utc) + expires_delta
    else:
        expire = datetime.now(tz=timezone.utc) + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, config.SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt



def create_refresh_token(data: dict, expires_delta: timedelta | None = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(days=REFRESH_TOKEN_EXPIRE_DAYS)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, config.SECRET_KEY_REFRESH, algorithm=ALGORITHM)
    return encoded_jwt
