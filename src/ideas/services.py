import uuid
from sqlmodel import select
from sqlmodel.ext.asyncio.session import AsyncSession
from src.db.models import Idea, Comment, Vote, Category, User
from src.errors import CategoryNotFound, UserNotFound
from src.ideas.schemas import IdeaCreationModel


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
