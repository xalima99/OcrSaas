from fastapi import APIRouter, Body, Depends, HTTPException, File, UploadFile, Request
from fastapi.encoders import jsonable_encoder
from typing import Optional, List

from app import crud, models, schemas
from app.api import deps
from app.db.client import AsyncIOMotorClient

from app.scripts.textract import detext_text

router = APIRouter()

@router.post('/')
async def get_infos(db: AsyncIOMotorClient = Depends(deps.get_db),
    current_user: models.User = Depends(deps.get_current_active_user), file: bytes = File(...)):
    #data = await request.body()
    '''if len(data) > 120:
        return "This file exceeds the maximum file size we support at this time 120",'''
    try:
        res = detext_text(file)
        return res

    except Exception as e:
        print(e)


# @router.post("/files")
# async def create_file(file: bytes = File(...)):
#     res = image_ocrer(file)
#     return res