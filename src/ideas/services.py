import uuid
from sqlmodel import select
from sqlmodel.ext.asyncio.session import AsyncSession
from src.db.models import Idea, Comment, Vote, Category, User
from src.errors import CategoryNotFound, IdeaNotFound, UserNotFound
from src.ideas.schemas import CommentCreationModel, IdeaCreationModel, VoteCreationModel


class IdeaServic:
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

    async def create_vote(self, vote_data: VoteCreationModel, session: AsyncSession):
        vote_data_dict = vote_data.model_dump()
        user = await session.exec(
            select(User).where(User.id == vote_data_dict["user_id"])
        )
        user = user.first()
        if user is None:
            raise UserNotFound
        idea = await session.exec(
            select(Idea).where(Idea.id == vote_data_dict["idea_id"])
        )
        idea = idea.first()
        if idea is None:
            raise IdeaNotFound
        vote = Vote(**vote_data_dict)
        session.add(vote)
        await session.commit()
        await session.refresh(vote)
        return vote

    async def update_vote(self, vote: Vote, vote_data: dict, session: AsyncSession):
        for k, v in vote_data.items():
            setattr(vote, k, v)
        await session.commit()
        return vote

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
