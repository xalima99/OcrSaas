from typing import Any, List

from fastapi import APIRouter, Body, Depends, HTTPException, status
from fastapi.encoders import jsonable_encoder
from pydantic.networks import EmailStr

from app import crud, models, schemas
from app.api import deps
from app.utils import send_confirmation_email, generate_verification_token
from app.db.client import AsyncIOMotorClient

router = APIRouter()

@router.post("/", response_model=schemas.User)
async def create_user(
    *,
    db: AsyncIOMotorClient = Depends(deps.get_db),
    user_in: schemas.UserCreate
) -> Any:
    """
    Create new user.
    """
    user = await crud.user.get_by_email(db, email=user_in.email)

    if user:
        raise HTTPException(
            status_code=400,
            detail="The user with this email already exists in the system.",
        )
    user = await crud.user.create(db, obj_in=user_in)
    user_data = jsonable_encoder(user)
    user = schemas.User(**user_data)
    return user
