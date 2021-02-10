from typing import Optional

from app.db.base_class import Base
from pydantic import BaseModel, EmailStr


# Shared properties
class UserBase(BaseModel):
    email: Optional[EmailStr] = None


# Properties to receive via API on creation
class UserCreate(UserBase):
    email: EmailStr
    password: str

class UserUpdate(UserBase):
    password: Optional[str] = None
    is_email_verified: Optional[bool] = None

class User(Base, UserBase):
    is_active: bool