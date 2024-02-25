from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app import schemas
from app.database.db import get_db
from app.exceptions.DataNotFoundException import DataNotFoundException
from app.exceptions.UserAlreadyExistsException import UserAlreadyExistsException
from app.security import BasicAuth
from app.services.UserService import user_service

router = APIRouter()


@router.get('/self', response_model=schemas.UserOut)
def get_user(current_user: Annotated[schemas.UserOut, Depends(BasicAuth.verification)],
             db: Session = Depends(get_db)):
    try:
        user = user_service.get_user_by_email_Id(username=current_user.username, db=db)
        print(user)
        if not user:
            raise DataNotFoundException(f"User with email: {id} Not Found!")
        return user
    except DataNotFoundException as e:
        raise HTTPException(status_code=404, detail=str(e))
    except Exception as e:
        print(e)
        raise HTTPException(status_code=500, detail='Internal Server Error')


@router.post('/', response_model=schemas.UserOut)
def register_user(user: schemas.UserCreate, db: Session = Depends(get_db)):
    try:
        print('inside post')
        data = user_service.get_user_by_email_Id(username=user.username, db=db)
        print('data ', data)
        if data is not None:
            raise UserAlreadyExistsException(f"User with email: {user.username} already registered!")
        data = user_service.create_user(user=user, db=db)
        return data

    except UserAlreadyExistsException as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        print(e)
        raise HTTPException(status_code=500, detail='Internal Server Error')


@router.put("/self",status_code=204)
def update_user(updateUser: schemas.UserCreate,
                current_user: Annotated[schemas.UserOut, Depends(BasicAuth.verification)],
                db: Session = Depends(get_db) ):
    try:
        if updateUser.username == current_user.username:
            user_service.update_user(updateUser=updateUser, db=db)
        else:
            raise HTTPException(status_code=403,
                                detail=f"User with {current_user.username} not authorized to perform requested action")

    except DataNotFoundException as e:
        raise HTTPException(status_code=404, detail=str(e))
    except Exception as e:
        print(e)
        raise HTTPException(status_code=500, detail='Internal Server Error')
