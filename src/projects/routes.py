from typing import List
import uuid
from fastapi import APIRouter, Depends
from sqlmodel.ext.asyncio.session import AsyncSession
from src.auth.dependencies import AccessTokenBearer
from src.db.main import get_session
from src.db.models import Project
from src.projects.services import ProjectService
from .schemas import ProjectUpdateModel, ProjectCreationModel
from src.errors import InvalidCredentials, ProjectNotFound, UserNotFound

project_router = APIRouter()
project_servie = ProjectService()


@project_router.get("/", response_model=List[Project])
async def get_all_projects(session: AsyncSession = Depends(get_session)):
    projects = await project_servie.get_all_projects(session)
    return projects


@project_router.get("/{project_id}", response_model=Project)
async def get_project_by_id(
    project_id: uuid.UUID, session: AsyncSession = Depends(get_session)
):
    project = await project_servie.get_project_by_id(project_id, session)
    if project is None:
        raise ProjectNotFound
    return project


@project_router.post("/", response_model=Project)
async def create_project(
    project_data: ProjectCreationModel,
    token: dict = Depends(AccessTokenBearer()),
    session: AsyncSession = Depends(get_session),
):
    if str(token["user"]["user_id"] != project_data.creator_id):
        raise InvalidCredentials
    project = await project_servie.create_project(project_data, session)
    return project


@project_router.put("/{project_id}", response_model=Project)
async def update_project(
    project_id: uuid.UUID,
    project_data: ProjectUpdateModel,
    token: dict = Depends(AccessTokenBearer()),
    session: AsyncSession = Depends(get_session),
):
    project = await project_servie.get_project_by_id(project_id, session)
    if project is None:
        raise ProjectNotFound
    if str(token["user"]["user_id"] != project.creator_id):
        raise InvalidCredentials

    updated_project = await project_servie.update_project(
        project, project_data, session
    )
    return updated_project


@project_router.delete("/{project_id}", response_model=Project)
async def delete_project(
    project_id: uuid.UUID,
    token: dict = Depends(AccessTokenBearer),
    session: AsyncSession = Depends(get_session),
):
    project = await project_servie.get_project_by_id(project_id, session)
    if project is None:
        raise ProjectNotFound

    if str(token["user"]["user_id"] != project.creator_id):
        raise InvalidCredentials

    deleted_project = await project_servie.delete_project(project_id, session)
    return deleted_project
