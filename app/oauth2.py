from jose import JWTError, jwt
from datetime import datetime, timedelta
from . import schemas, database, models
from fastapi import status, Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session
from .config import settings

oauth2_scheme = OAuth2PasswordBearer(tokenUrl='login') # declate the end point of the login function by the url and the user's token

SECRET_KEY = settings.secret_key
ALGORITHM = settings.algorithm
ACCESS_TOKEN_EXPIRE_MINUTES = settings.access_token_expire_minutes

def creare_access_token(data: dict):
    to_encode = data.copy()

    expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    
    to_encode.update({"expire" : expire.isoformat()}) #datetime is not JSON serialized so we need ro convert it it an Object that is. ISO for example

    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)

    return encoded_jwt


def verify_access_token(token: str , credentials_execption):
    try:
        payload = jwt.decode(token=token, key=SECRET_KEY,algorithms=[ALGORITHM])

        id: str = payload.get("user_id") #cause when we created the token(in auth.py) we added the user_id as additional data
        if id is None:
            raise credentials_execption
        token_data = schemas.TokenData(id=id)

    except JWTError:
        raise credentials_execption
    
    return token_data


def get_current_user(token: str = Depends(oauth2_scheme), db: Session = Depends(database.get_db)):
    credentials_execption = HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                                          detail=f"Could not validate credentials", headers={"WWW=Authenticate": "Bearer"})
    
    token = verify_access_token(token,credentials_execption)
    user = db.query(models.User).filter(models.User.id == token.id == id).first()
    return user

# the idea of the having the get_curent_user function for authenticate a user instead of just having the vetify_access_token
#(which is possible just to have that) is the fact that we can fetch the user from the data base and attach the user to
# any path operation and preform any logic we want based on the id(what the vrify_access_token returns)