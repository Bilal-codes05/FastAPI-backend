from fastapi import FastAPI ,Depends,status,Response,HTTPException
from typing import List
from sqlalchemy.orm import Session
import models
from database import engine,get_db
import schemas
from hashing import Hash
from routers import blog

app=FastAPI()


models.Base.metadata.create_all(bind=engine)

app.include_router(blog.router)

# # dependency to get db session
# def get_db():
#     db=sessionlocal()
#     try:
#         yield db
#     finally:
#         db.close()



@app.post("/blog",status_code=status.HTTP_201_CREATED,tags=['blogs'])
def create(request:schemas.Blog,db:Session=Depends(get_db)):
    new_blog=models.Blog(title=request.title, body=request.body,user_id=1)
    db.add(new_blog)
    db.commit()
    db.refresh(new_blog)
    return new_blog


# # This endpoint is used to get all blogs
# @app.get("/blog",response_model=List[schemas.BlogResponse],tags=['blogs'])
# def all_blogs(db:Session=Depends(get_db)):
#     blogs=db.query(models.Blog).all()
#     return blogs



# This endpoint is used to get a specific blog by id
@app.get("/blog/{id}",status_code=200,response_model=schemas.BlogResponse,tags=['blogs'])
def show(id, response:Response ,db:Session=Depends(get_db)):
    blog=db.query(models.Blog).filter(models.Blog.id==id).first()
    if not blog:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"Blog with the id {id} is not available")
        # response.status_code=status.HTTP_404_NOT_FOUND
        # return {"details":f"Blog with the id {id} is not available"}
    return blog


# This endpoint is used to delete a blog by id
@app.delete("/blog",tags=['blogs'])
def delete_blog(id:int ,db:Session=Depends(get_db)):
    blog=db.query(models.Blog).filter(models.Blog.id==id).delete()
    if not blog:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail=
                            f"Blog with the id {id} is not found")
    
    db.commit()
    return {"success":"blog deleted successfully"}
 



# this is endpoint is used to update a blog by id 
@app.put("/blog/{id}", status_code=status.HTTP_202_ACCEPTED, response_model=List[schemas.BlogResponse],tags=['blogs'])
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


# Users end points
@app.post("/user" , response_model=schemas.ShowUser,tags=['users'])
def create_user(request:schemas.User, db:Session=Depends(get_db)):
    new_user=models.User(name=request.name, email=request.email, password=Hash.bcrypt(request.password))
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user


@app.get("/user/{id}", response_model=schemas.ShowUser,tags=['users'])
def get_user(id:int, db:Session=Depends(get_db)):
    user=db.query(models.User).filter(models.User.id==id).first()
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"User with the id {id} is not available")
    return user


  

