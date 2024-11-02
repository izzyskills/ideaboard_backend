import uuid
from sqlmodel.ext.asyncio.session import AsyncSession
from sqlmodel import select

from src.db.models import Project, User
from src.errors import ProjectNotFound, UserNotFound
from src.projects.schemas import ProjectCreationModel, ProjectUpdateModel


class ProjectService:
    async def get_project_by_id(self, project_id: uuid.UUID, session: AsyncSession):
        statement = select(Project).where(Project.id == project_id)

        result = await session.exec(statement)

        project = result.first()

        if project is None:
            raise ProjectNotFound

        return project

    async def project_exists(self, project_id: uuid.UUID, session: AsyncSession):
        project = await self.get_project_by_id(project_id, session)

        return True if project is not None else False

    async def create_project(
        self, project_data: ProjectCreationModel, session: AsyncSession
    ):
        project_data_dict = project_data.model_dump()

        created_by_id = project_data_dict["created_by"]
        user = await session.exec(select(User).where(User.id == created_by_id))
        user = user.first()
        if user is None:
            raise UserNotFound

        new_project = Project(
            **{
                "title": project_data_dict["title"],
                "description": project_data_dict["description"],
                "url": project_data_dict["url"],
                "creator_id": project_data_dict["creator_id"],
            }
        )
        session.add(new_project)
        await session.commit()
        return new_project

    async def update_project(
        self, project: Project, project_data: ProjectUpdateModel, session: AsyncSession
    ):
        project_data_dict = project_data.model_dump()

        for k, v in project_data_dict.items():
            setattr(project, k, v)

        await session.commit()

        return project

    async def delete_project(self, project_id: uuid.UUID, session: AsyncSession):
        project = await self.get_project_by_id(project_id, session)

        await session.delete(project)

        await session.commit()

        return project
