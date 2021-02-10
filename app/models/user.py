from typing import Optional

from app.db.base_class import Base, PyObjectId

class User(Base):
    email: str
    hashed_password: str
    is_email_verified: bool
    is_active: bool
