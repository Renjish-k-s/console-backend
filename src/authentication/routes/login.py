from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from src.database import get_db
from src.authentication.schema.login import LoginResponse
from src.authentication.utils.auth import authenticate_user, ACCESS_TOKEN_EXPIRE_MINUTES,create_access_token, create_refresh_token, verify_refresh_token, decode_access_token,oauth2_scheme
from src.tenent.models.user import User
from fastapi.security import OAuth2PasswordRequestForm
from fastapi import Request
from datetime import timedelta
from datetime import datetime, timedelta, timezone
from src.authentication.models.invalidtoken import InvalidToken
#libraries for rate limiting
from slowapi import Limiter
from slowapi.util import get_remote_address
from fastapi import Request

limiter = Limiter(key_func=get_remote_address)


router = APIRouter(
    prefix="/auth",
    tags=["authentication"]
)



@router.post("/login",response_model=LoginResponse)
@limiter.limit("2/minute")  # Appling a rate limit of n requests per minute
async def login_for_access_token(
    request: Request,
    form_data: OAuth2PasswordRequestForm = Depends(),
    db: AsyncSession = Depends(get_db)
):
    user = await authenticate_user(db, form_data.username, form_data.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password"
        )
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token =  create_access_token(
        data={"sub": user.email}, expires_delta=access_token_expires
    )
    refresh_token =  create_refresh_token(data={"sub": user.email})

    return LoginResponse(
        access_token=access_token,
        refresh_token=refresh_token,
        token_type="Bearer"
    )



@router.post("/refresh", response_model=LoginResponse)
async def refresh_token(refresh_token: str, db: AsyncSession = Depends(get_db)):
    username = verify_refresh_token(refresh_token)
    if not username:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid refresh token"
        )

    # Optionally check if user still exists
    result = await db.execute(select(User).filter(User.email == username))
    user = result.scalars().first()
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="User not found"
        )

    # create new access token
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": user.email}, expires_delta=access_token_expires
    )
    # optionally rotate refresh token
    new_refresh_token = create_refresh_token(data={"sub": user.email})

    return LoginResponse(
        access_token=access_token,
        refresh_token=new_refresh_token,
        token_type="Bearer"
    )



@router.post("/logout", status_code=status.HTTP_204_NO_CONTENT)
async def logout(
    token: str = Depends(oauth2_scheme),
    db: AsyncSession = Depends(get_db)
):
    payload = decode_access_token(token)
    if not payload:
        raise HTTPException(status_code=401, detail="Invalid token")

    jti = payload.get("jti")
    exp = payload.get("exp")

    if not jti or not exp:
        raise HTTPException(status_code=401, detail="Invalid token")

    db.add(
        InvalidToken(
            jti=jti,
            expires_at=datetime.fromtimestamp(exp, tz=timezone.utc)
        )
    )
    await db.commit()
