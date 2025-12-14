from pydantic import BaseModel, EmailStr


class OTPCreate(BaseModel):
    email: EmailStr

class OTPVerify(BaseModel):
    email: EmailStr
    otp: str


