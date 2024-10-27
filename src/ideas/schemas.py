import uuid
from pydantic import BaseModel
from typing import List, Optional


class IdeaCreationModel(BaseModel):
    title: str
    description: str
    category_id: uuid.UUID
    creator_id: uuid.UUID
    catergory_name: str


class CommentCreationModel(BaseModel):
    content: str
    user_id: uuid.UUID
    idea_id: uuid.UUID


class VoteCreationModel(BaseModel):
    user_id: uuid.UUID
    idea_id: uuid.UUID
    is_upvote: bool
