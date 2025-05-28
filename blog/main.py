from fastapi import FastAPI ,Depends,status,Response,HTTPException
from sqlalchemy.orm import Session
import models
from database import engine,sessionlocal
import schemas


app=FastAPI()


models.Base.metadata.create_all(bind=engine)

# dependency to get db session
def get_db():
    db=sessionlocal()
    try:
        yield db
    finally:
        db.close()



@app.post("/blog",status_code=status.HTTP_201_CREATED,response_model=schemas.BlogResponse)
def create(request:schemas.Blog,db:Session=Depends(get_db)):
    new_blog=models.Blog(title=request.title, body=request.body)
    db.add(new_blog)
    db.commit()
    db.refresh(new_blog)
    return new_blog

# This endpoint is used to get all blogs
@app.get("/blog")
def all_blogs(db:Session=Depends(get_db)):
    blogs=db.query(models.Blog).all()
    return blogs

# This endpoint is used to get a specific blog by id
@app.get("/blog/{id}",status_code=200)
def show(id, response:Response ,db:Session=Depends(get_db)):
    blog=db.query(models.Blog).filter(models.Blog.id==id).first()
    if not blog:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"Blog with the id {id} is not available")
        # response.status_code=status.HTTP_404_NOT_FOUND
        # return {"details":f"Blog with the id {id} is not available"}
    return blog


# This endpoint is used to delete a blog by id
@app.delete("/blog")
def delete_blog(id:int ,db:Session=Depends(get_db)):
    db.query(models.Blog).filter(models.Blog.id==id).delete(synchronize_session=False)
    db.commit()
    return {"success":"blog deleted successfully"}

