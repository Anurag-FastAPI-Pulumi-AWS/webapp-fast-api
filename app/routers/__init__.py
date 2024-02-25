from fastapi import APIRouter
from . import User

api_router = APIRouter()

api_router.include_router(User.router, prefix="/v1/users",
                          tags=['Users'])
