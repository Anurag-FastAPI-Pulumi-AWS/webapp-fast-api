from typing import Any

from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm import Session

from app import models, schemas
from app.util import passutil


class userService:

    def get_user_by_email_Id(self, username: str, db: Session) -> Any:
        """ Get User Data based on email"""
        try:
            data = db.query(models.User).filter(
                models.User.username == username).first()
            return data
        except SQLAlchemyError as e:
            print(e)
            return None

    def update_user(self, updateUser: schemas.UserCreate, db: Session) -> Any:
        """ Get User Data based on email"""
        # try:
        #     update_query = db.query(models.User).filter(models.User.username == updateUser.username)
        #     update_query.update(updateUser.dict())
        #     db.commit()
        #     return update_query.first()
        # except SQLAlchemyError as e:
        #     return None

        try:
            db_user = db.query(models.User).filter(
                models.User.username == updateUser.username).first()
            hashed_password = passutil.get_password_hash(str(updateUser.password))
            db_user.first_name = updateUser.first_name
            db_user.last_name = updateUser.last_name
            db_user.username = updateUser.username
            db_user.password = hashed_password
            db.commit()
            db.refresh(db_user)
            return db_user
        except SQLAlchemyError as e:
            return None

    def create_user(self, user: schemas.UserCreate, db: Session) -> Any:
        """ Get User Data based on email"""
        try:
            hashed_password = passutil.get_password_hash(str(user.password))
            db_user = models.User(username=user.username,
                                  password=hashed_password,
                                  first_name=user.first_name,
                                  last_name=user.last_name,
                                  )
            db.add(db_user)
            db.commit()
            db.refresh(db_user)
            return db_user
        except SQLAlchemyError as e:
            print(e)
            return None


user_service = userService()