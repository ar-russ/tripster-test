from sqlalchemy import Column, Integer, ForeignKey, Enum

from src.models.db.base import Base
from src.enums.rating import VoteType


class Vote(Base):
    __tablename__ = "votes"

    id: int = Column(Integer, primary_key=True)
    user_id: int = Column(ForeignKey("user.id"))
    post_id: int = Column(ForeignKey("posts.id"))
    type: str = Column(Enum(*VoteType.values(), name="vote_type"))
