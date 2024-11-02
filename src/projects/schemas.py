import uuid
from pydantic import BaseModel, Field


class ProjectCreationModel(BaseModel):
    name: str
    description: str
    url: str
    creator_id: uuid.UUID


class ProjectUpdateModel(BaseModel):
    name: str | None = None
    description: str | None = None
    url: str | None = None
