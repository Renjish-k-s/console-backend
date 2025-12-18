from fastapi import FastAPI, HTTPException, status

from src.authentication.routes import register, login
from src.tenent.routes import user_management


from slowapi import Limiter
from slowapi.util import get_remote_address
from slowapi.errors import RateLimitExceeded
from fastapi.responses import JSONResponse


from fastapi import FastAPI, Request
from datetime import datetime
import asyncio
from src.database import get_db, AsyncSessionLocal


limiter = Limiter(key_func=get_remote_address)




app=FastAPI(
    title="Console Backend",
    version="v0",
    decription="Backend for Console Application",
    )

from fastapi.middleware.cors import CORSMiddleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],        # allow all origins (dev only)
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)



app.state.limiter = limiter  # required
# Rate limit exception handler
@app.exception_handler(RateLimitExceeded)
async def rate_limit_handler(request, exc):
    raise HTTPException(
        status_code=status.HTTP_429_TOO_MANY_REQUESTS,
        detail="Rate limit exceeded"
    )

# Required middleware
from slowapi.middleware import SlowAPIMiddleware
app.add_middleware(SlowAPIMiddleware)

app.include_router(register.router)
app.include_router(login.router)
app.include_router(user_management.router)
