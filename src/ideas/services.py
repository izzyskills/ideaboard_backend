from datetime import datetime
import uuid
from sqlmodel import and_, select
from sqlmodel.ext.asyncio.session import AsyncSession
from src.db.models import Idea, Comment, Vote, Category, User
from src.errors import CategoryNotFound, IdeaNotFound, UserNotFound, VoteNotFound
from src.ideas.schemas import CommentCreationModel, IdeaCreationModel, VoteCreationModel


class IdeaService:
    async def create_idea(self, idea_data: IdeaCreationModel, session: AsyncSession):
        idea_data_dict = idea_data.model_dump()

        # get user it
        created_by_id = idea_data_dict["created_by"]
        user = await session.exec(select(User).where(User.id == created_by_id))
        user = user.first()
        if user is None:
            raise UserNotFound
        if idea_data_dict["category_id"] == -1:
            new_category = Category(**{"name": idea_data_dict["category_name"]})
            idea_data_dict["category_id"] = new_category.id
        else:
            category = (
                await session.exec(
                    select(Category).where(Category.id == idea_data_dict["category_id"])
                )
            ).first()
            if category is None:
                raise CategoryNotFound

        new_idea = Idea(**idea_data_dict)
        session.add(new_idea)
        await session.commit()
        await session.refresh(new_idea)

        return new_idea

    async def get_idea_by_id(self, idea_id: uuid.UUID, session: AsyncSession):
        idea = await session.exec(select(Idea).where(Idea.id == idea_id))
        idea = idea.first()
        return idea

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

    async def get_vote_counts(self, idea_id: uuid.UUID, session: AsyncSession) -> dict:
        result = await session.exec(select(Vote).where(Vote.idea_id == idea_id))
        votes = result.scalars().all()

        upvotes = sum(1 for vote in votes if vote.is_upvote)
        downvotes = sum(1 for vote in votes if not vote.is_upvote)

        return {
            "idea_id": str(idea_id),
            "upvotes": upvotes,
            "downvotes": downvotes,
            "total": len(votes),
            "score": upvotes - downvotes,
        }

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
        existing_vote = result.scalar_one_or_none()

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
        vote = result.scalar_one_or_none()

        if vote:
            await session.delete(vote)
            await session.commit()
            return vote

        raise VoteNotFound
