from pydantic import BaseModel, EmailStr


class OTPCreate(BaseModel):
    email: EmailStr

class OTPVerify(BaseModel):
    email: EmailStr
    otp: str

class TenentCreate(BaseModel):
    organization_name: str
    admin_email: EmailStr
    admin_username: str
    admin_password: str

