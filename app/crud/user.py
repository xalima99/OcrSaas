from typing import Any, Dict, Optional, Union

from app.core.settings import MONGO_DB
from app.core.security import get_password_hash, verify_password
from app.crud.base import CRUDBase
from app.db.client import AsyncIOMotorClient
from app.db.base_class import PyObjectId
from app.models.user import User
from app.schemas.user import UserCreate, UserUpdate


class CRUDuser(CRUDBase[User, UserCreate, UserUpdate]):
    async def get_by_email(self, db: AsyncIOMotorClient, *, email: str) -> Optional[User]:
        print("DB GET BY MAIL", db)
        data = await db[MONGO_DB][self.collection].find_one({"email": email})
        db_obj = User(**data) if data else None
        return db_obj
        
    def create(self, db: AsyncIOMotorClient, *, obj_in: UserCreate) -> User:
        
        db_obj = User(
            email=obj_in.email,
            hashed_password=get_password_hash(obj_in.password),
            is_email_verified=False,
            is_active=True
        )
        
        return super().create(db, obj_in=db_obj)
    
    def update(self, db: AsyncIOMotorClient, *, db_obj: User, obj_in: Union[UserUpdate, Dict[str, Any]]
               ) -> User:
        if isinstance(obj_in, dict):
            update_data = obj_in
        else:
            update_data = obj_in.dict(exclude_unset=True)
        if 'password' in update_data and update_data['password']:
            hashed_password = get_password_hash(update_data['password'])
            del update_data['password']
            update_data['hashed_password'] = hashed_password
        return super().update(db, db_obj=db_obj, obj_in=update_data)
    
    async def authenticate(self, db: AsyncIOMotorClient, *, email: str, password: str) -> Optional[User]:
        user = await self.get_by_email(db, email=email)
        print("authenticate user get by email", user)
        if user is None:
            return None
        if not verify_password(password, user.hashed_password):
            return None
        return user
    
    def is_active(self, user: User) -> bool:
        return user.is_active
    
    def is_email_verified(self, user: User) -> bool:
        return user.is_email_verified
    

user = CRUDuser(User)