from bson import ObjectId
from datetime import datetime
from typing import Optional

from pydantic import BaseModel, Field

class PyObjectId(ObjectId):

    @classmethod
    def __get_validators__(cls):
        yield cls.validate

    @classmethod
    def validate(cls, v):
        if not ObjectId.is_valid(v):
            raise ValueError('Invalid objectid')
        return ObjectId(v)

    @classmethod
    def __modify_schema__(cls, field_schema):
        field_schema.update(type='string')


class Base(BaseModel):
    id: Optional[PyObjectId] = Field(alias='_id')
    created_on: datetime = datetime.now()
    updated_on: datetime = None

    __name__: str

    def __collection_name__(cls) -> str:
        return cls.__name__.lower()

    class Config:
        arbitrary_types_allowed = True
        json_encoders = {
            ObjectId: str
        }