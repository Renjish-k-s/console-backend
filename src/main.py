from fastapi import FastAPI

from src.authentication.routes import register



app=FastAPI(
    title="Console Backend",
    version="v0",
    decription="Backend for Console Application",
    )


app.include_router(register.router)
