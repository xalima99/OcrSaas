from bson import ObjectId
from datetime import datetime
from typing import Any, Dict, Generic, List, Optional, Type, TypeVar, Union, Tuple

from fastapi.encoders import jsonable_encoder
from pydantic import BaseModel

from app.db.client import AsyncIOMotorClient
from app.db.base_class import Base
from app.core.settings import MONGO_DB

ModelType = TypeVar("ModelType", bound=Base)
CreateSchemaType = TypeVar("CreateSchemaType", bound=BaseModel)
UpdateSchemaType = TypeVar("UpdateSchemaType", bound=BaseModel)

class CRUDBase(Generic[ModelType, CreateSchemaType, UpdateSchemaType]):
    def __init__(self, model: Type[ModelType]):
        """
        CRUD object with default methods to Create, Read, Update, Delete (CRUD).
        **Parameters**

        * `model`: A MongoDB model class
        * `schema`: A Pydantic model (schema) class
        """
        self.model = model
        self.collection = self.model.__collection_name__(model)
        
    async def get(self, db: AsyncIOMotorClient, id: Any) -> Optional[ModelType]:
        data = await db[MONGO_DB][self.collection].find_one({"_id": ObjectId(id)})
        db_obj = self.model(**data) if data else None
        return db_obj
    
    async def get_many(self, db: AsyncIOMotorClient, fields: Dict, skip: int = 0, limit: int = 100
    ) -> List[ModelType]:
        return db[MONGO_DB][self.collection].find(fields).skip(skip).limit(limit)
    
    async def create(self, db: AsyncIOMotorClient, *, obj_in: CreateSchemaType) -> ModelType:
        obj_in_data = jsonable_encoder(obj_in)
        db_obj = self.model(**obj_in_data)
        del db_obj.id
        insert_result = await db[MONGO_DB][self.collection].insert_one(db_obj.dict())
        db_obj.id = insert_result.inserted_id
        return db_obj
    
    async def update(self, db: AsyncIOMotorClient, *, db_obj: ModelType, 
    obj_in: Union[UpdateSchemaType, Dict[str, any]]) -> ModelType:
        if isinstance(obj_in, dict):
            update_data = obj_in
        else:
            update_data = obj_in.dict(exclude_unset=True)
            
        update_data['updated_on'] = datetime.now()
        await db[MONGO_DB][self.collection].update_one({"_id": db_obj.id}, {"$set": update_data})
        return db_obj
    
    async def remove(self, db: AsyncIOMotorClient, *, db_obj:ModelType) -> ModelType:
        obj = await db[MONGO_DB][self.collection].delete_one({"_id": db_obj.id})
        return obj
    
    async def remove_by_any_field(self, db: AsyncIOMotorClient, *, field: Tuple) -> ModelType:
        print("Field Remove", field, field[0], field[1])
        obj = await db[MONGO_DB][self.collection].delete_one({field[0]: field[1]})
        return obj
        
        