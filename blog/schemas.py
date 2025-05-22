from pydantic import BaseModel

class Blog(BaseModel):
    title:str
    body:str
    
class BlogResponse(BaseModel):
    title:str
    body:str
    class config:
        orm_mode=True
    
    