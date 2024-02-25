from typing import Annotated

from fastapi import Depends, HTTPException
from fastapi.security import HTTPBasic, HTTPBasicCredentials
from sqlalchemy.orm import Session

from app.database.db import get_db
from app.exceptions.AuthorizationException import AuthorizationException
from app.services.UserService import user_service
from app.util import passutil

security = HTTPBasic()


def verification(creds: Annotated[HTTPBasicCredentials, Depends(security)], db: Session = Depends(get_db)):
    try:
        username = creds.username
        password = creds.password
        userObj = user_service.get_user_by_email_Id(username=username, db=db)
        if userObj is not None:
            if hasattr(userObj, 'password') and passutil.verify_password(password,userObj.password) :
                return userObj
            else:
                raise AuthorizationException("Incorrect email or password")
        else:
            raise AuthorizationException("Incorrect email or password")
    except AuthorizationException as e:
        raise HTTPException(status_code=401, detail=str(e))
    except Exception as e:
        print("Auth exception", e)
        raise HTTPException(status_code=500, detail="Internal Server Error")
