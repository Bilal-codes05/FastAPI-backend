from fastapi import FastAPI
from pydantic import BaseModel


app=FastAPI()

class Blog(BaseModel):
    name:str
    age:int
    id:str

@app.post("/blog")
def create(request:Blog):
    return request
    
@app.get("/get")
def read(id:int):
    return {"id":id}

@app.put("/update")
def update():
    return "updating a blog post"

@app.delete("/delete")
def delete():
    return "Deleting a blog post"



