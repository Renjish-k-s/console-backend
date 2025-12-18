from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from src.database import get_db
from src.authentication.utils.auth import oauth2_scheme,decode_access_token
from src.tenent.schema.tenent_user import CreateTenentUserSchema, TokenData
from src.tenent.models.user import User
from src.authentication.utils.auth import get_current_active_user
from src.authentication.utils.utils import hash_password
from fastapi.responses import JSONResponse

router = APIRouter(
    prefix="/Tenent",
    tags=["Tenent"]
)

@router.post("/usercreate")
async def create_user(
    details: CreateTenentUserSchema,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_active_user),
):
    # Check email exists
    email_query = await db.execute(
        select(User).where(User.email == details.email)
    )
    if email_query.scalar_one_or_none():
        return JSONResponse(
            status_code=status.HTTP_400_BAD_REQUEST,
            content={"error": "Email already exists"},
        )

    # Check username exists
    username_query = await db.execute(
        select(User).where(User.username == details.full_name)
    )
    if username_query.scalar_one_or_none():
        return JSONResponse(
            status_code=status.HTTP_400_BAD_REQUEST,
            content={"error": "Username already exists"},
        )

    hashed_password = hash_password(details.password)

    new_user = User(
        email=details.email,
        username=details.full_name,
        hashed_password=hashed_password,
        tenent_id=current_user.tenent_id,
    )

    db.add(new_user)
    await db.commit()
    await db.refresh(new_user)

    return JSONResponse(
        status_code=status.HTTP_201_CREATED,
        content={
            "msg": "User created successfully",
            "user_id": new_user.id,
        },
    )




