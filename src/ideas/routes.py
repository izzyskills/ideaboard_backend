import uuid
from fastapi import WebSocket
from fastapi import APIRouter, HTTPException
from fastapi.param_functions import Depends
from sqlmodel.ext.asyncio.session import AsyncSession
from src.auth.dependencies import AccessTokenBearer
from src.errors import IdeaIdMismatch, IdeaNotFound, InvalidCredentials, UserNotFound
from .services import IdeaService
from .schemas import IdeaCreationModel, VoteCreationModel, CommentCreationModel
from src.db.main import get_session

idea_router = APIRouter()
idea_service = IdeaService()


@idea_router.post("/")
async def create_idea(
    idea_data: IdeaCreationModel,
    token: dict = Depends(AccessTokenBearer()),
    session: AsyncSession = Depends(get_session),
):
    if str(token["user"]["user_id"]) != idea_data.creator_id:
        raise InvalidCredentials
    idea = await idea_service.create_idea(idea_data, session)
    return idea


@idea_router.get("/{idea_id}")
async def get_idea_by_id(
    idea_id: uuid.UUID, session: AsyncSession = Depends(get_session)
):
    idea = await idea_service.get_idea_by_id(idea_id, session)
    if idea is None:
        raise IdeaNotFound
    return idea


@idea_router.post("/{idea_id}/vote")
async def make_vote(
    idea_id: uuid.UUID,
    vote_data: VoteCreationModel,
    token: dict = Depends(AccessTokenBearer()),
    session: AsyncSession = Depends(get_session),
):
    if str(token["user"]["user_id"]) != vote_data.user_id:
        raise InvalidCredentials
    if idea_id != vote_data.idea_id:
        raise IdeaIdMismatch
    vote = await idea_service.create_vote(vote_data, session)
    return vote


@idea_router.post("/{idea_id}/comment")
async def make_comment(
    idea_id: uuid.UUID,
    comment_data: CommentCreationModel,
    token: dict = Depends(AccessTokenBearer()),
    session: AsyncSession = Depends(get_session),
):
    if str(token["user"]["user_id"]) != comment_data.user_id:
        raise InvalidCredentials
    if idea_id != comment_data.idea_id:
        raise IdeaIdMismatch
    comment = await idea_service.create_comment(comment_data, session)
    return comment


@idea_router.websocket("/{idea_id}/vote/details")
async def get_vote_details(
    websocket: WebSocket,
    idea_id: uuid.UUID,
    session: AsyncSession = Depends(get_session),
):
    await websocket.accept()
    vote_details = await idea_service.get_vote_details(idea_id, session)
    await websocket.send_json(vote_details)
