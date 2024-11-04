from datetime import datetime
from typing import Dict, List, Optional, Tuple
import uuid
from sqlmodel import and_, desc, func, or_, select, case
from sqlmodel.sql.expression import Select
from sqlmodel.ext.asyncio.session import AsyncSession
from src.db.models import Idea, Comment, Project, Vote, Category, User
from src.errors import (
    CategoryNotFound,
    IdeaNotFound,
    ProjectNotFound,
    UserNotFound,
    VoteNotFound,
)
from src.ideas.schemas import (
    CommentCreationModel,
    IdeaCreationModel,
    IdeaSearchParams,
    VoteCreationModel,
)


class IdeaService:
    async def create_idea(self, idea_data: IdeaCreationModel, session: AsyncSession):
        idea_data_dict = idea_data.model_dump()

        # get user it
        created_by_id = idea_data_dict["creator_id"]
        user = await session.exec(select(User).where(User.id == created_by_id))
        user = user.first()
        if user is None:
            raise UserNotFound

        # Validate categories
        category_ids = idea_data_dict["category_ids"]
        categories = await session.exec(
            select(Category).where(Category.id.in_(category_ids))
        )
        categories = categories.all()
        if len(categories) != len(category_ids):
            raise CategoryNotFound

        # Validate project
        project_id = idea_data_dict["project_id"]
        project = await session.exec(select(Project).where(Project.id == project_id))
        project = project.one_or_none()
        if project is None:
            raise ProjectNotFound

        # Create new idea
        new_idea = Idea(
            **{
                "title": idea_data_dict["title"],
                "description": idea_data_dict["description"],
                "creator_id": idea_data_dict["creator_id"],
                "project_id": idea_data_dict["project_id"],
                "categories": categories,
            }
        )
        session.add(new_idea)
        await session.commit()
        await session.refresh(new_idea)

        return new_idea

    async def search_ideas(
        self,
        session: AsyncSession,
        params: IdeaSearchParams,
        current_user_id: Optional[uuid.UUID] = None,
    ) -> Tuple[List[Dict], Optional[uuid.UUID]]:
        try:
            # Start with base query for ideas
            query = (
                select(
                    Idea,
                    Project.name.label("project_name"),
                    User.username.label("creator_username"),
                    func.count(Vote.id)
                    .filter(Vote.is_upvote.is_(True))
                    .label("upvotes"),
                    func.count(Vote.id)
                    .filter(Vote.is_upvote.is_(False))
                    .label("downvotes"),
                    func.count(
                        case(
                            (
                                and_(
                                    Vote.user_id == current_user_id,
                                    Vote.is_upvote.is_(True),
                                ),
                                1,
                            )
                        )
                    ).label("user_upvoted"),
                    func.count(
                        case(
                            (
                                and_(
                                    Vote.user_id == current_user_id,
                                    Vote.is_upvote.is_(False),
                                ),
                                1,
                            )
                        )
                    ).label("user_downvoted"),
                )
                .select_from(Idea)
                .outerjoin(Vote)
                .join(Project, Project.id == Idea.project_id)
                .join(User, User.id == Idea.creator_id)
                .group_by(Idea.id, Project.id, User.id)
            )

            filters = []

            # Category filter
            if params.category_ids:
                filters.append(
                    Idea.categories.any(Category.id.in_(params.category_ids))
                )

            # Debug print for project_id
            print(f"Project ID: {params.project_id}")

            # Project filter
            if params.project_id:
                filters.append(Idea.project_id == params.project_id)

            # Text search using the pre-computed search_vector
            if params.text:
                search_query = f"%{params.text}%"
                filters.append(
                    or_(
                        Idea.title.ilike(search_query),
                        Idea.description.ilike(search_query),
                    )
                )
            # Cursor pagination
            if params.cursor:
                print(f"Cursor: {params.cursor}")
                filters.append(Idea.created_at < params.cursor)

            # Apply all filters
            if filters:
                query = query.where(and_(*filters))

            # Debug print for final query
            print(f"Final Query: {query}")

            # Add ordering and limit
            query = query.order_by(desc(Idea.created_at)).limit(params.limit)

            # Execute query
            results = await session.execute(query)
            rows = results.all()

            # Debug print for query results
            print(f"Query Results: {rows}")

            # Process results into dictionaries
            ideas_with_votes = []
            for row in rows:
                idea = row[0]  # The Idea object
                idea_dict = {
                    "id": str(idea.id),
                    "title": idea.title,
                    "description": idea.description,
                    "project_id": str(idea.project_id),
                    "project_name": row.project_name,
                    "creator_id": str(idea.creator_id),
                    "creator_username": row.creator_username,
                    "created_at": idea.created_at.isoformat(),
                    "votes": {
                        "upvotes": row.upvotes,
                        "downvotes": row.downvotes,
                        "total": row.upvotes + row.downvotes,
                        "score": row.upvotes - row.downvotes,
                    },
                }

                # Add user's vote status if user_id was provided
                if current_user_id:
                    idea_dict["user_vote"] = {
                        "has_voted": bool(row.user_upvoted or row.user_downvoted),
                        "is_upvote": (
                            bool(row.user_upvoted)
                            if (row.user_upvoted or row.user_downvoted)
                            else None
                        ),
                    }

                ideas_with_votes.append(idea_dict)

            # Calculate next cursor
            next_cursor = rows[-1][0].created_at if len(rows) == params.limit else None

            return ideas_with_votes, next_cursor

        except Exception as e:
            print(f"Search error: {str(e)}")

    async def create_comment(
        self, comment_data: CommentCreationModel, session: AsyncSession
    ):
        comment_data_dict = comment_data.model_dump()
        user = await session.exec(
            select(User).where(User.id == comment_data_dict["user_id"])
        )
        user = user.first()
        if user is None:
            raise UserNotFound
        idea = await session.exec(
            select(Idea).where(Idea.id == comment_data_dict["idea_id"])
        )
        idea = idea.first()
        if idea is None:
            raise IdeaNotFound
        comment = Comment(**comment_data_dict)
        session.add(comment)
        await session.commit()
        await session.refresh(comment)
        return comment

    async def handle_vote(
        self,
        idea_id: uuid.UUID,
        user_id: uuid.UUID,
        vote_data: VoteCreationModel,
        session: AsyncSession,
    ) -> Vote:
        # Check for existing vote
        result = await session.exec(
            select(Vote).where(and_(Vote.idea_id == idea_id, Vote.user_id == user_id))
        )
        existing_vote = result.one_or_none()

        if existing_vote:
            # Update existing vote if different
            if existing_vote.is_upvote != vote_data.is_upvote:
                existing_vote.is_upvote = vote_data.is_upvote
                existing_vote.updated_at = datetime.utcnow()
                await session.commit()
            return existing_vote
        else:
            # Create new vote
            new_vote = Vote(
                **{
                    "user_id": user_id,
                    "idea_id": idea_id,
                    "is_upvote": vote_data.is_upvote,
                }
            )
            session.add(new_vote)
            await session.commit()
            return new_vote

    async def delete_vote(
        self, idea_id: uuid.UUID, user_id: uuid.UUID, session: AsyncSession
    ):
        result = await session.exec(
            select(Vote).where(and_(Vote.idea_id == idea_id, Vote.user_id == user_id))
        )
        vote = result.one_or_none()

        if vote:
            await session.delete(vote)
            await session.commit()
            return vote

        raise VoteNotFound
