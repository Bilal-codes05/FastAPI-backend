from fastapi import FastAPI 
import models
from database import engine
from routers import blog,user,authentication

app=FastAPI(
    tags=['Login']
)


models.Base.metadata.create_all(bind=engine)

app.include_router(authentication.router)
app.include_router(blog.router)
app.include_router(user.router)



# # dependency to get db session
# def get_db():
#     db=sessionlocal()
#     try:
#         yield db
#     finally:
#         db.close()






# # This endpoint is used to get all blogs
# @app.get("/blog",response_model=List[schemas.BlogResponse],tags=['blogs'])
# def all_blogs(db:Session=Depends(get_db)):
#     blogs=db.query(models.Blog).all()
#     return blogs




# Users end points

