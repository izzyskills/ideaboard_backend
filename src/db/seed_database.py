import asyncio
from sqlmodel import SQLModel
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker
from datetime import datetime, timedelta
import uuid
import os
import random
from typing import List, Dict
from models import Category, Idea, User, Project, Vote, Comment

# Replace with your database URL
DATABASE_URL = os.getenv("DATABASE_URL")

# Create async engine
engine = create_async_engine(
    DATABASE_URL, echo=True  # Set to False to disable SQL logging
)

# Create async session maker
async_session = sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)


def random_date():
    days_back = random.randint(0, 365)
    return datetime.utcnow() - timedelta(days=days_back)


async def create_users_projects_categories() -> Dict[str, List]:
    # Create categories with fixed IDs
    categories = [
        Category(id=1, name="AI/ML"),
        Category(id=2, name="FrontEnd"),
        Category(id=3, name="Backend"),
        Category(id=4, name="FullStack"),
        Category(id=5, name="Mobile"),
        Category(id=6, name="GameDev"),
        Category(id=7, name="DevOps"),
        Category(id=8, name="Cloud"),
        Category(id=9, name="DataScience"),
        Category(id=10, name="Security"),
        Category(id=11, name="IoT"),
        Category(id=12, name="Blockchain"),
        Category(id=13, name="AR/VR"),
        Category(id=14, name="Other"),
    ]

    # Create 5 users with fixed UUIDs
    user_ids = [uuid.uuid4() for _ in range(5)]
    users = [
        User(
            id=user_id,
            username=f"user{i}",
            email=f"user{i}@example.com",
            password_hash=f"hashed_password_{i}",
            is_verified=True,
            created_at=random_date(),
        )
        for i, user_id in enumerate(user_ids, 1)
    ]

    # Create 3 projects with fixed UUIDs
    project_data = [
        (
            "FastAPI",
            "A modern, fast web framework for building APIs with Python",
            "https://fastapi.tiangolo.com",
        ),
        ("GIMP", "GNU Image Manipulation Program", "https://www.gimp.org"),
        (
            "Arch Linux",
            "A lightweight and flexible Linux distribution",
            "https://archlinux.org",
        ),
    ]

    project_ids = [uuid.uuid4() for _ in range(len(project_data))]
    projects = [
        Project(
            id=project_id,
            name=name,
            description=desc,
            url=url,
            creator_id=random.choice(user_ids),
            creted_at=random_date(),
        )
        for (name, desc, url), project_id in zip(project_data, project_ids)
    ]

    return {
        "categories": categories,
        "users": users,
        "projects": projects,
        "user_ids": user_ids,
        "project_ids": project_ids,
    }


async def create_ideas(
    user_ids: List[uuid.UUID], project_ids: List[uuid.UUID], categories: List[Category]
) -> List[Idea]:
    # Create 10 ideas
    idea_titles = [
        "Add OAuth2 Support",
        "Implement Dark Mode",
        "Mobile App Integration",
        "Performance Optimization",
        "Cloud Deployment Tools",
        "Security Enhancements",
        "User Dashboard",
        "API Documentation",
        "Automated Testing",
        "Community Features",
    ]

    idea_ids = [uuid.uuid4() for _ in range(len(idea_titles))]
    ideas = []

    for idea_id, title in zip(idea_ids, idea_titles):
        idea = Idea(
            id=idea_id,
            title=title,
            description=f"Detailed description for {title}",
            project_id=random.choice(project_ids),
            creator_id=random.choice(user_ids),
            created_at=random_date(),
        )
        idea.categories = random.sample(categories, random.randint(2, 3))
        ideas.append(idea)

    return ideas


async def create_votes_comments(
    user_ids: List[uuid.UUID], idea_ids: List[uuid.UUID]
) -> Dict[str, List]:
    # Create 10 comments
    comments = [
        Comment(
            id=uuid.uuid4(),
            content=f"This is comment {i} on the idea",
            user_id=random.choice(user_ids),
            idea_id=random.choice(idea_ids),
            created_at=random_date(),
        )
        for i in range(1, 11)
    ]

    # Create 20 votes
    votes = []
    for _ in range(20):
        idea_id = random.choice(idea_ids)
        user_id = random.choice(user_ids)
        is_upvote = random.choice([True, True, True, False])  # 75% chance of upvote

        vote = Vote(
            id=uuid.uuid4(), user_id=user_id, idea_id=idea_id, is_upvote=is_upvote
        )
        votes.append(vote)

    return {
        "comments": comments,
        "votes": votes,
    }


async def init_db():
    async with engine.begin() as conn:
        await conn.run_sync(SQLModel.metadata.drop_all)
        await conn.run_sync(SQLModel.metadata.create_all)


async def main():
    # Initialize database
    await init_db()

    # Create users, projects, and categories
    data = await create_users_projects_categories()

    # Insert categories first
    async with async_session() as session:
        for category in data["categories"]:
            session.add(category)
        await session.commit()

        # Insert users
        for user in data["users"]:
            session.add(user)
        await session.commit()

        # Insert projects
        for project in data["projects"]:
            session.add(project)
        await session.commit()

    # Create ideas
    ideas = await create_ideas(
        data["user_ids"], data["project_ids"], data["categories"]
    )

    # Insert ideas
    async with async_session() as session:
        for idea in ideas:
            session.add(idea)
        await session.commit()

    # Create votes and comments
    idea_ids = [idea.id for idea in ideas]
    votes_comments = await create_votes_comments(data["user_ids"], idea_ids)

    # Insert comments
    async with async_session() as session:
        for comment in votes_comments["comments"]:
            session.add(comment)
        await session.commit()

        # Insert votes
        for vote in votes_comments["votes"]:
            session.add(vote)
        await session.commit()

        print("\nData insertion completed successfully!")
        print(f"Created {len(data['users'])} users")
        print(f"Created {len(data['projects'])} projects")
        print(f"Created {len(ideas)} ideas")
        print(f"Created {len(votes_comments['comments'])} comments")
        print(f"Created {len(votes_comments['votes'])} votes")


if __name__ == "__main__":
    asyncio.run(main())
