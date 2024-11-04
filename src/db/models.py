import uuid
from sqlmodel import (
    Computed,
    ForeignKey,
    Index,
    SQLModel,
    Field,
    Relationship,
    Column,
    Table,
)
from typing import Optional, List
from datetime import datetime
import sqlalchemy.dialects.postgresql as pg


# User Model
class User(SQLModel, table=True):
    id: uuid.UUID = Field(
        sa_column=Column(pg.UUID, nullable=False, primary_key=True, default=uuid.uuid4)
    )
    username: str = Field(index=True, unique=True)
    email: str = Field(index=True, unique=True)
    created_at: datetime = Field(
        sa_column=Column(pg.TIMESTAMP, default=datetime.utcnow())
    )
    is_verified: bool = Field(default=False)
    password_hash: str
    ideas: List["Idea"] = Relationship(back_populates="creator")
    comments: List["Comment"] = Relationship(back_populates="user")
    votes: List["Vote"] = Relationship(back_populates="user")
    projects: List["Project"] = Relationship(back_populates="creator")


# Project Model
class Project(SQLModel, table=True):
    id: uuid.UUID = Field(
        sa_column=Column(pg.UUID, nullable=False, primary_key=True, default=uuid.uuid4)
    )

    name: str = Field(unique=True)
    description: str
    url: str
    creator_id: uuid.UUID = Field(foreign_key="user.id")
    creted_at: datetime = Field(
        sa_column=Column(pg.TIMESTAMP, default=datetime.utcnow())
    )

    ideas: List["Idea"] = Relationship(back_populates="project")
    creator: User = Relationship(back_populates="projects")


class IdeaCategoryAssociation(SQLModel, table=True):
    idea_id: uuid.UUID = Field(
        sa_column=Column(pg.UUID, ForeignKey("idea.id"), primary_key=True)
    )
    category_id: int = Field(ForeignKey("category.id"), primary_key=True)


class Category(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    name: str
    ideas: List["Idea"] = Relationship(
        back_populates="categories",
        link_model=IdeaCategoryAssociation,
        sa_relationship_kwargs={
            "primaryjoin": "Category.id == IdeaCategoryAssociation.category_id",
            "secondaryjoin": "Idea.id == IdeaCategoryAssociation.idea_id",
        },
    )


class Idea(SQLModel, table=True):
    id: uuid.UUID = Field(
        sa_column=Column(pg.UUID, nullable=False, primary_key=True, default=uuid.uuid4)
    )
    title: str
    description: str
    project_id: uuid.UUID = Field(foreign_key="project.id")
    creator_id: uuid.UUID = Field(foreign_key="user.id")
    created_at: datetime = Field(
        sa_column=Column(pg.TIMESTAMP, default=datetime.utcnow())
    )
    creator: User = Relationship(back_populates="ideas")
    project: Project = Relationship(back_populates="ideas")
    categories: List["Category"] = Relationship(
        back_populates="ideas",
        link_model=IdeaCategoryAssociation,
        sa_relationship_kwargs={
            "primaryjoin": "Idea.id == IdeaCategoryAssociation.idea_id",
            "secondaryjoin": "Category.id == IdeaCategoryAssociation.category_id",
        },
    )
    comments: List["Comment"] = Relationship(back_populates="idea")
    votes: List["Vote"] = Relationship(back_populates="idea")
    search_vector: str = Field(
        sa_column=Column(
            pg.TSVECTOR,
            Computed(
                "to_tsvector('english', title || ' ' || description)", persisted=True
            ),
        )
    )
    __table_args__ = (
        Index("idx_idea_search_vector", "search_vector", postgresql_using="gin"),
    )


# Comment Model
class Comment(SQLModel, table=True):
    id: uuid.UUID = Field(
        sa_column=Column(pg.UUID, nullable=False, primary_key=True, default=uuid.uuid4)
    )
    content: str
    user_id: uuid.UUID = Field(foreign_key="user.id")
    idea_id: uuid.UUID = Field(foreign_key="idea.id")
    created_at: datetime = Field(
        sa_column=Column(pg.TIMESTAMP, default=datetime.utcnow())
    )
    user: User = Relationship(back_populates="comments")
    idea: Idea = Relationship(back_populates="comments")


# Vote Model
class Vote(SQLModel, table=True):
    id: uuid.UUID = Field(
        sa_column=Column(pg.UUID, nullable=False, primary_key=True, default=uuid.uuid4)
    )
    user_id: uuid.UUID = Field(foreign_key="user.id")
    idea_id: uuid.UUID = Field(foreign_key="idea.id")
    is_upvote: bool  # True for upvote, False for downvote

    user: User = Relationship(back_populates="votes")
    idea: Idea = Relationship(back_populates="votes")
