import uuid

from sqlalchemy import Column, String, TIMESTAMP, text, func, UUID
from sqlalchemy.dialects import postgresql

from app.database.db import Base


class User(Base):
    __tablename__ = "User"
    id = Column(postgresql.UUID(as_uuid=True),
                primary_key=True,
                default=uuid.uuid4,
                unique=True
                )
    first_name = Column(String, nullable=False)
    last_name = Column(String, nullable=False)
    password = Column(String, nullable=False)
    username = Column(String, nullable=False, unique=True)
    account_created = Column(TIMESTAMP(timezone=True), nullable=False, server_default=text('now()'))
    account_updated = Column(TIMESTAMP(timezone=True), server_default=text('now()'),
                             onupdate=func.now())
