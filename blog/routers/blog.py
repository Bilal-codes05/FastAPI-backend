from fastapi import APIRouter,Depends,status,HTTPException,Response
from typing import List
from sqlalchemy.orm import Session
import database,models,schemas
from hashing import Hash
from oauth import get_current_user

get_db=database.get_db

router=APIRouter(
    tags=['Blogs']
)

# This endpoint is used to get all blogs
@router.get("/blog",response_model=List[schemas.BlogResponse])
def all_blogs(db:Session=Depends(get_db),get_current_user:schemas.User=Depends(get_current_user)):
    blogs=db.query(models.Blog).all()
    return blogs

@router.post("/blog",status_code=status.HTTP_201_CREATED)
def create(request:schemas.Blog,db:Session=Depends(get_db)):
    new_blog=models.Blog(title=request.title, body=request.body,user_id=1)
    db.add(new_blog)
    db.commit()
    db.refresh(new_blog)
    return new_blog

# This endpoint is used to get a specific blog by id
@router.get("/blog/{id}",status_code=200,response_model=schemas.BlogResponse)
def show(id,db:Session=Depends(get_db)):
    blog=db.query(models.Blog).filter(models.Blog.id==id).first()
    if not blog:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"Blog with the id {id} is not available")
        # response.status_code=status.HTTP_404_NOT_FOUND
        # return {"details":f"Blog with the id {id} is not available"}
    return blog


# This endpoint is used to delete a blog by id
@router.delete("/blog")
def delete_blog(id:int ,db:Session=Depends(get_db)):
    blog=db.query(models.Blog).filter(models.Blog.id==id).delete()
    if not blog:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail=
                            f"Blog with the id {id} is not found")
    
    db.commit()
    return {"success":"blog deleted successfully"}
 



# this is endpoint is used to update a blog by id 
@router.put("/blog/{id}", status_code=status.HTTP_202_ACCEPTED, response_model=List[schemas.BlogResponse])
def update(id: int, request: schemas.Blog, db: Session = Depends(get_db)):
    blog = db.query(models.Blog).filter(models.Blog.id == id).first()
    
    if not blog:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"Blog with id {id} not found")
    
    blog.title=request.title
    blog.body=request.body
    db.commit()
    db.refresh(blog)
    
    return blog

