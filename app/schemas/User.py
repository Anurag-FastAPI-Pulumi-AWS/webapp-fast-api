import uuid
from datetime import datetime
from typing import Optional

from pydantic import BaseModel, EmailStr


class UserOut(BaseModel):
    id: uuid.UUID
    first_name: str
    last_name: str
    username: EmailStr
    account_created: datetime
    account_updated: Optional[datetime]

    class Config:
        orm_mode = True


class UserCreate(BaseModel):
    first_name: str
    last_name: str
    username: EmailStr
    password: str

    class Config:
        orm_mode = True
