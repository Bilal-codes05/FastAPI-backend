from fastapi import APIRouter,Depends,status,HTTPException
import schemas
import database,models,auth_token
from sqlalchemy.orm import Session
from hashing import Hash

router=APIRouter(
    
    tags=['Authentication']
)

@router.post('/login')
def login(request:schemas.Login,db:Session=Depends(database.get_db)):
    user=db.query(models.User).filter(models.User.email==request.username).first()
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"Invalid credentials")
    if not Hash.verify(user.password,request.password):
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"Incorrect Password")
        
        
 
    access_token = auth_token.create_access_token(data={"sub": user.email})
    return {"access token":access_token , "token type ":"bearer"}
