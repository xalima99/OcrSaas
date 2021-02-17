from datetime import timedelta
from typing import Any

from fastapi import APIRouter, Body, Depends, HTTPException
from fastapi.security import OAuth2PasswordRequestForm
from fastapi.encoders import jsonable_encoder

from app import crud, models, schemas
from app.api import deps
from app.core import security
from app.core import settings
from app.utils import check_verification_token, generate_verification_token, send_reset_password_email
from app.db.client import AsyncIOMotorClient


router = APIRouter()

@router.post("/login", response_model=schemas.Token)
async def login(
    db: AsyncIOMotorClient = Depends(deps.get_db), form_data: OAuth2PasswordRequestForm = Depends()
) -> Any:
    """
    OAuth2 compatible token login, get an access token for future requests
    """
    user = await crud.user.authenticate(
        db, email=form_data.username, password=form_data.password
    )
    print("BBB")
    if not user:
        print("1BBB")
        raise HTTPException(status_code=400, detail="Incorrect email or password")
    elif not crud.user.is_active(user):
        print("2BBB")
        raise HTTPException(status_code=400, detail="Inactive user")
    # elif not crud.user.is_email_verified(user):
    #     print("3BBB")
    #     raise HTTPException(status_code=400, detail="Email not verified")
    access_token_expires = timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    print("ACCESS TOKEN EXPIRES")
    return {
        "access_token": security.create_access_token(user.id),
        "token_type": "bearer",
    }
    
@router.get("/verify-email", response_model=schemas.Msg)
async def verify_email(token: str, db: AsyncIOMotorClient = Depends(deps.get_db)
) -> Any:
    """
    Verify Email
    """
    email = check_verification_token(token)
    if not email:
        raise HTTPException(status_code=400, detail="Invalid Token")
    user = await crud.user.get_by_email(db, email=email)
    if not user:
        raise HTTPException(
            status_code=404,
            detail="The user with this email does not exist in the system."
        )
    elif not crud.user.is_active(user):
        raise HTTPException(status_code=400, detail="Inactive user")
    user_in = schemas.UserUpdate(**jsonable_encoder(user))
    user_in.is_email_verified = True
    user = await crud.user.update(db, db_obj=user, obj_in=user_in)
    return {"msg": "Email verified successfully"}

@router.get("/password-recovery/{email}", response_model=schemas.Msg)
async def recover_password(email: str, db: AsyncIOMotorClient = Depends(deps.get_db)):
    """
    Password Recovery
    """
    user = await crud.user.get_by_email(db, email=email)

    if not user:
        raise HTTPException(
            status_code=404,
            detail="The user with this email does not exist in the system.",
        )
    password_reset_token = generate_verification_token(email)
    send_reset_password_email(email=email, token=password_reset_token)
    return {"msg": "Password recovery email sent"}


@router.post("/reset-password/", response_model=schemas.Msg)
async def reset_password(
    token: str = Body(...),
    new_password: str = Body(...),
    db: AsyncIOMotorClient = Depends(deps.get_db),
) -> Any:
    """
    Reset password
    """
    email = check_verification_token(token)
    if not email:
        raise HTTPException(status_code=400, detail="Invalid token")
    user = await crud.user.get_by_email(db, email=email)
    if not user:
        raise HTTPException(
            status_code=404,
            detail="The user with this email does not exist in the system.",
        )
    elif not crud.user.is_active(user):
        raise HTTPException(status_code=400, detail="Inactive user")
    #hashed_password = security.get_password_hash(new_password)
    user_in = schemas.UserUpdate(**jsonable_encoder(user))
    user_in.password = new_password
    user = await crud.user.update(db=db, db_obj=user, obj_in=user_in)
    return {"msg": "Password updated successfully"}