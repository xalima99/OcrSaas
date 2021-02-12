from fastapi import FastAPI

from starlette.middleware.gzip import GZipMiddleware
from starlette.responses import Response

from app.api.api import router as endpoints_router
from app.db.client import db_close, db_connect, AsyncIOMotorClient
from app.payment import payment_router

app = FastAPI(title="ocr", version="1.0")
app.add_middleware(GZipMiddleware, minimum_size=1000)

app.include_router(endpoints_router)
app.include_router(payment_router, tags=["Payments"])



@app.on_event("startup")
async def on_app_start():
    """
    Anything that needs to be done while app starts
    """
    await db_connect()


@app.on_event("shutdown")
async def on_app_shutdown():
    """
    Anything that needs to be done while app shutdown
    """
    await db_close()


@app.get("/")
async def home():
    """
    Home page
    """
    return Response("Welcome to OcrAS")