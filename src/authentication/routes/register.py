from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from src.database import get_db
from src.authentication.schema.register import OTPCreate, OTPVerify
from src.authentication.utils.utils import generate_otp
from datetime import datetime, timedelta
from src.authentication.utils.mailer import send_email
from src.authentication.models.otp import OTP

router = APIRouter(
    prefix="/auth",
    tags=["authentication"]
)
RESEND_TIME_LIMIT = timedelta(minutes=2)




@router.post("/sendotp")
async def send_otp(
    otp: OTPCreate,
    db: AsyncSession = Depends(get_db)
):
    result = await db.execute(select(OTP).filter(OTP.email == otp.email,OTP.is_used == False))
    db_otp = result.scalars().first()

    if db_otp:
        now = datetime.utcnow()  
        updated_at = db_otp.updated_at
        time_diff = now - updated_at

        # Less than 10 min block
        if time_diff < RESEND_TIME_LIMIT:
            minutes_left = int((RESEND_TIME_LIMIT - time_diff).total_seconds() // 60)
            raise HTTPException(
                status_code=status.HTTP_429_TOO_MANY_REQUESTS,
                detail=f"OTP already sent. Try again in {minutes_left} minutes."
            )
        else:
        # More than 10 min  resend same OTP
            otp_tosend=generate_otp()
            if(send_email(db_otp.email, otp_tosend)):
                db_otp.updated_at = datetime.utcnow()
                db_otp.otp = otp_tosend
                await db.commit()
                await db.refresh(db_otp)
                
                return {"detail": "OTP resent successfully"}

            else:
                raise HTTPException(
                    status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                    detail="Failed to send OTP"
                )
    else:
        otp_tosend=generate_otp()
        if(send_email(otp.email, otp_tosend)):

            # No OTP exists  create new one
            new_otp = OTP(
                email=otp.email,
                otp=otp_tosend,
                is_used=False
            )
            db.add(new_otp)
            await db.commit()
            await db.refresh(new_otp)

            return {"detail": "OTP Sent successfully"}

        else:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Failed to send OTP"
            )


@router.post("/verifyotp")
async def send_otp(
    otp: OTPVerify,
    db: AsyncSession = Depends(get_db)
):
    result = await db.execute(
        select(OTP).filter(
            OTP.email == otp.email,
            OTP.is_used == False
        )
    )
    db_otp = result.scalars().first()

    if not db_otp:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="No OTP found for this email"
        )

    # EXPIRY CHECK (20 minutes)
    if datetime.utcnow() - db_otp.updated_at > timedelta(minutes=20):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="OTP expired"
        )

    if db_otp.otp != otp.otp:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid OTP"
        )

    db_otp.is_used = True
    await db.commit()
    await db.refresh(db_otp)

    return {"detail": "OTP verified successfully"}
