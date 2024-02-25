from fastapi import FastAPI, HTTPException, Depends
from fastapi.exceptions import RequestValidationError
from sqlalchemy.orm import Session
from starlette import status
from starlette.requests import Request
from starlette.responses import JSONResponse

from app.database.db import get_db, engine, Base
from app.routers import api_router

try:
    Base.metadata.create_all(bind=engine)
except Exception as e:
    print("DB connection error ", e)

app = FastAPI()


@app.get("/healthz")
async def root(db: Session = Depends(get_db)):
    try:
        return {"message": "Hello world!!"}
    except Exception as e:
        raise HTTPException(status_code=503, detail=str(e))


app.include_router(api_router)
print("SUCCESS!")


@app.exception_handler(RequestValidationError)
async def request_validation_exception_handler(request: Request, exc: RequestValidationError):
    return JSONResponse(
        status_code=status.HTTP_405_METHOD_NOT_ALLOWED,
        headers={"Cache-Control": "no-cache, no-store, must-revalidate", "Pragma": "no-cache",
                 "X-Content-Type-Options": "nosniff"},
    )

