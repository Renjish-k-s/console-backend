from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from src.database import get_db
from src.authentication.schema.login import LoginRequest, LoginResponse
from src.authentication.utils.auth import authenticate_user, ACCESS_TOKEN_EXPIRE_MINUTES,create_access_token, create_refresh_token
from fastapi.security import OAuth2PasswordRequestForm
from fastapi import Request
from datetime import timedelta

router = APIRouter(
    prefix="/auth",
    tags=["authentication"]
)



@router.post("/login",response_model=LoginResponse)
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

