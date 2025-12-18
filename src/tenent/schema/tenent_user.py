from pydantic import BaseModel, EmailStr
from typing import Optional

class CreateTenentUserSchema(BaseModel):
    email: EmailStr
    full_name: str
    password: str
    share_pass: bool = False

class TokenData(BaseModel):
    username: Optional[str] = None