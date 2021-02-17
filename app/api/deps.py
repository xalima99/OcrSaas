from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from jose import jwt
from pydantic import ValidationError

from app import crud, models, schemas
from app.schemas.token import TokenPayload
from app.core.security import ALGORITHM
from app.core.settings import SECRET_KEY
from app.db.client import get_db, AsyncIOMotorClient

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/login")

async def get_current_user(
    db: AsyncIOMotorClient = Depends(get_db), token: str = Depends(oauth2_scheme)
) -> models.User:
    # print("get_current_user")
    try:
        payload = jwt.decode(
            token, SECRET_KEY, algorithms=[ALGORITHM]
        )
        token_data = TokenPayload(**payload)
    except (jwt.JWTError, ValidationError) as e:
        message = getattr(e, 'message', repr(e))
        print("EXCEPT", message)
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Could not validate credentials"
        )
    # print("Token sub id", token_data.sub)
    user = await crud.user.get(db, id=token_data.sub)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user

def get_current_active_user(
    current_user: models.User = Depends(get_current_user),
) -> models.User:
    # print("Get current active user")
    if not crud.user.is_active(current_user):
        raise HTTPException(status_code=400, detail="Inactive user")
    return current_user