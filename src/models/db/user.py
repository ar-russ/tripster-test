from fastapi_users.db import SQLAlchemyBaseUserTable
from sqlalchemy import Column, Integer
from sqlalchemy.orm import relationship

from src.models.db.base import Base


class User(SQLAlchemyBaseUserTable, Base):
    id: int = Column(Integer, primary_key=True)
    posts = relationship("Post", back_populates="author")
