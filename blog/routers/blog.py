from fastapi import APIRouter,Depends
from typing import List
from sqlalchemy.orm import Session
import database,models,schemas


router=APIRouter()

# This endpoint is used to get all blogs
@router.get("/blog",response_model=List[schemas.BlogResponse],tags=['blogs'])
def all_blogs(db:Session=Depends(database.get_db)):
    blogs=db.query(models.Blog).all()
    return blogs