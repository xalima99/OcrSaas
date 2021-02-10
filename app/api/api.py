from fastapi import APIRouter

from app.api.endpoints import login, users

router = APIRouter()
router.include_router(login.router, tags=["Login"])
router.include_router(users.router, prefix="/users", tags=["Users"])