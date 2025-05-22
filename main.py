from fastapi import FastAPI   #type:ignore
from typing import Optional
from pydantic import BaseModel #type:ignore
import uvicorn


app=FastAPI()

@app.get("/blog")
def show(limit=10,published:bool=True, sort:Optional[str]=None):
    if published:
        return {"data":f"{limit} published blogs from the database"}
    else:
        return {"data":f"{limit} published blogs from the database"}

 
@app.get("/about")
def about():
    return { "data": {"name":"Bilal Rafique",
            "age":22,
            "city":"Karachi"}}
@app.get("/blog/Unpublished")
def published():
    return {"data":"Hello my name is Bilal Rafique, I am 22 years old and I live in Samundari."}

@app.get("/blog/{id}")
def blog(id:int):
    return {"data": id}

@app.get("/blog/{id}/comments")
def comments(id,limit=10):
    return limit
    return {"data":{'1','2'}}

@app.get("/blog/{id}/comments/{comment_id}")
def comment_id(id:int, comment_id:str):
    return {"data":{id,comment_id}}


class Blog(BaseModel):
    title:str
    body:str
    published: Optional[bool]



@app.post("/blog")
def create_blog(request:Blog):
    return {"data": f"Blog is created with title {request.title} and body {request.body} and published status is {request.published}"}




if __name__=="__main__":
    uvicorn.run(app, host="127.0.0.1", port=9000)
    