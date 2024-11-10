from datetime import datetime
import uuid
from pydantic import BaseModel
from typing import List, Optional


class IdeaCreationModel(BaseModel):
    title: str
    description: str
    category_id: int
    creator_id: uuid.UUID
    project_id: uuid.UUID


class CommentCreationModel(BaseModel):
    content: str
    user_id: uuid.UUID
    idea_id: uuid.UUID


class VoteCreationModel(BaseModel):
    is_upvote: bool


class IdeaSearchParams(BaseModel):
    project_id: Optional[uuid.UUID] = None
    category_ids: Optional[List[int]] = None
    text: Optional[str] = None
    limit: Optional[int] = 10
    cursor: Optional[datetime] = None
