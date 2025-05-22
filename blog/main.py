from fastapi import FastAPI ,Depends
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



@app.post("/blog",response_model=schemas.BlogResponse)
def create(request:schemas.Blog,db:Session=Depends(get_db)):
    new_blog=models.Blog(title=request.title, body=request.body)
    db.add(new_blog)
    db.commit()
    db.refresh(new_blog)
    return new_blog
