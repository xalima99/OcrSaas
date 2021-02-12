# load environment variables from root path 
import os
from dotenv import load_dotenv
print(os.getcwd())
load_dotenv(os.path.join(os.getcwd(), ".env"))


from fastapi import APIRouter
from app.api.endpoints import login, users

router = APIRouter()
router.include_router(login.router, tags=["Login"])
router.include_router(users.router, prefix="/users", tags=["Users"])