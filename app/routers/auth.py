from fastapi import APIRouter, HTTPException, Depends,status,Response
from fastapi.security.oauth2 import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from .. import database, schemas, models, utils, oauth2



router = APIRouter(tags=['Authentication'])

@router.post("/login",response_model=schemas.Token)
def login(user_credentails: OAuth2PasswordRequestForm = Depends() ,db: Session = Depends(database.get_db)):



    # the OAuth2PasswordRequestForm return a dict with 2 items:
    # {
    #       "username" : "some user name"  ------ in our case is the email
    #       "password" : "some password"   ------ our password
    # }

    user = db.query(models.User).filter(models.User.email == user_credentails.username).first()
    
    if not user:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail=f" Invalid Email or Password.")
    
    if not utils.verify(user_credentails.password ,user.password):
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail=f" Invalid Email or Password.")

    #create a token and return it
    access_token = oauth2.creare_access_token(data={"user_id" : user.id})   # the data is the data we want to put in the payload, we can put more than jsut the id

    return{"access_token": access_token, "token_type" : "bearer" }
