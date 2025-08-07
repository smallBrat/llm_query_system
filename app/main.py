# app/main.py

from fastapi import FastAPI
from app.routes import router

app = FastAPI(title="HackRx Query System")
app.include_router(router, prefix="/api/v1")
