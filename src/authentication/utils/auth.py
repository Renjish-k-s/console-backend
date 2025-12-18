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
import uuid
from src.tenent.schema.tenent_user import TokenData

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


def create_access_token(
    data: Dict[str, str],
    expires_delta: Optional[timedelta] = None
) -> str:
    to_encode = data.copy()
    to_encode["jti"] = str(uuid.uuid4())

    expire = datetime.now(tz=timezone.utc) + (
        expires_delta or timedelta(minutes=15)
    )
    to_encode.update({"exp": expire})

    return jwt.encode(to_encode, config.SECRET_KEY, algorithm=ALGORITHM)


def create_refresh_token(
    data: Dict[str, str],
    expires_delta: Optional[timedelta] = None
) -> str:
    to_encode = data.copy()
    to_encode["jti"] = str(uuid.uuid4())

    expire = datetime.now(tz=timezone.utc) + (
        expires_delta or timedelta(days=REFRESH_TOKEN_EXPIRE_DAYS)
    )
    to_encode.update({"exp": expire})

    return jwt.encode(
        to_encode, config.SECRET_KEY_REFRESH, algorithm=ALGORITHM
    )

# ----------

def verify_refresh_token(token: str):
    try:
        payload = jwt.decode(token, config.SECRET_KEY_REFRESH, algorithms=ALGORITHM)
        username: str = payload.get("sub")
        if username is None:
            return None
        return username
    except jwt.JWTError:
        return None
    


def decode_access_token(token: str) -> dict | None:
    try:
        return jwt.decode(
            token, config.SECRET_KEY, algorithms=[ALGORITHM]
        )
    except JWTError:
        return None


def decode_refresh_token(token: str) -> dict | None:
    try:
        return jwt.decode(
            token, config.SECRET_KEY_REFRESH, algorithms=[ALGORITHM]
        )
    except JWTError:
        return None
    


async def get_current_user(token: str = Depends(oauth2_scheme), db: AsyncSession = Depends(get_db)) -> User:
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials"
    )
    try:
        payload = jwt.decode(token, config.SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub")
        if username is None:
            raise credentials_exception
        token_data = TokenData(username=username)
    except JWTError:
        raise credentials_exception

    result = await db.execute(select(User).filter(User.email == token_data.username))
    user = result.scalars().first()
    if user is None:
        raise credentials_exception
    return user


async def get_current_active_user(current_user: User = Depends(get_current_user)) -> User:
    """You can have some custom logic about the User.
    Here I am chcking the User is active or not."""
    if not current_user.is_active:
        raise HTTPException(status_code=400, detail="Inactive user")
    return current_user
