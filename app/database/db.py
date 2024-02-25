from fastapi import HTTPException
from sqlalchemy import create_engine, text
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

from app.config import settings

# SQLALCHEMY_DATABASE_URL = "postgresql://user:password@postgresserver/db"

SQLALCHEMY_DATABASE_URL = f'postgresql://{settings.DATABASE_USERNAME}:{settings.DATABASE_PASSWORD}@{settings.DATABASE_HOSTNAME}:{settings.DATABASE_PORT}/{settings.DATABASE_NAME}'
engine = create_engine(
        SQLALCHEMY_DATABASE_URL
    )
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


Base = declarative_base()


def get_db():
    try:
        db = SessionLocal()
        db.execute(text('SELECT 1')).fetchall()
        yield db
    except SQLAlchemyError as e:
        print(f"Error establishing DB connection: {e}")
        raise HTTPException(status_code=503, detail="Service Unavailable")
    finally:
        if db:
            db.close()