from datetime import datetime

from pydantic import BaseModel


class GetPost(BaseModel):
    body: str
    created: datetime
    author_id: int
    votes_amount: int
    rating: int


class CreatePost(BaseModel):
    body: str
