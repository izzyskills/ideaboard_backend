import uuid
from pydantic import BaseModel
from typing import List, Optional


class IdeaCreationModel(BaseModel):
    title: str
    description: str
    category_ids: List[int]
    creator_id: uuid.UUID
    catergory_name: str
    project_id: uuid.UUID


class CommentCreationModel(BaseModel):
    content: str
    user_id: uuid.UUID
    idea_id: uuid.UUID


class VoteCreationModel(BaseModel):
    is_upvote: bool


class IdeaSearchParams(BaseModel):
    category_ids: Optional[List[int]] = None
    project_id: Optional[uuid.UUID] = None
    text: Optional[str] = None
    limit: Optional[int] = 10
    cursor: Optional[uuid.UUID] = None
