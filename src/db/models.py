from sqlmodel import SQLModel, Field, Relationship, Column
from typing import Optional, List
from datetime import datetime
import sqlalchemy.dialects.postgresql as pg


# User Model
class User(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
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


# Idea Model
class Idea(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    title: str
    description: str
    category_id: int = Field(foreign_key="category.id")
    creator_id: int = Field(foreign_key="user.id")
    created_at: datetime = Field(
        sa_column=Column(pg.TIMESTAMP, default=datetime.utcnow())
    )
    vote_count: int = Field(default=0, index=True)

    creator: User = Relationship(back_populates="ideas")
    category: "Category" = Relationship(back_populates="ideas")
    comments: List["Comment"] = Relationship(back_populates="idea")
    votes: List["Vote"] = Relationship(back_populates="idea")


# Comment Model
class Comment(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    content: str
    user_id: int = Field(foreign_key="user.id")
    idea_id: int = Field(foreign_key="idea.id")
    created_at: datetime = Field(
        sa_column=Column(pg.TIMESTAMP, default=datetime.utcnow())
    )
    user: User = Relationship(back_populates="comments")
    idea: Idea = Relationship(back_populates="comments")


# Vote Model
class Vote(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    user_id: int = Field(foreign_key="user.id")
    idea_id: int = Field(foreign_key="idea.id")
    is_upvote: bool  # True for upvote, False for downvote

    user: User = Relationship(back_populates="votes")
    idea: Idea = Relationship(back_populates="votes")


# Category Model
class Category(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    name: str = Field(unique=True)
    ideas: List[Idea] = Relationship(back_populates="category")
