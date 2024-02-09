from datetime import datetime

from sqlalchemy import Column, Integer, String, TIMESTAMP, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func

from src.models.db.base import Base


class Post(Base):
    __tablename__ = "posts"

    id: int = Column(Integer, primary_key=True)
    body: str = Column(String)

    author_id: int = Column(ForeignKey("user.id"))
    author = relationship("User", back_populates="posts")

    created: datetime = Column(TIMESTAMP, server_default=func.now())
