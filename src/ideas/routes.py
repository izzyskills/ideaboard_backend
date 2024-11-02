from typing import List, Optional, Tuple
import uuid
from fastapi import WebSocket, WebSocketDisconnect
from fastapi import APIRouter, HTTPException
from fastapi.param_functions import Depends
from sqlmodel.ext.asyncio.session import AsyncSession
from src.auth.dependencies import AccessTokenBearer
from src.db.models import Idea
from src.errors import IdeaIdMismatch, IdeaNotFound, InvalidCredentials, UserNotFound
from src.ideas.managers import VoteConnectionManager
from .services import IdeaService
from .schemas import (
    IdeaCreationModel,
    IdeaSearchParams,
    VoteCreationModel,
    CommentCreationModel,
)
from src.db.main import get_session

idea_router = APIRouter()
idea_service = IdeaService()
vote_manager = VoteConnectionManager()


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


@idea_router.get("/ideas/search", response_model=Tuple[List[Idea], Optional[uuid.UUID]])
async def search_ideas_route(
    params: IdeaSearchParams = Depends(), session: AsyncSession = Depends(get_session)
):
    return await idea_service.search_ideas(session, params)


@idea_router.get("/{idea_id}")
async def get_idea_by_id(
    idea_id: uuid.UUID, session: AsyncSession = Depends(get_session)
):
    idea = await idea_service.get_idea_by_id(idea_id, session)
    if idea is None:
        raise IdeaNotFound
    return idea


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


@idea_router.websocket("/{idea_id}/votes/ws")
async def vote_websocket(
    websocket: WebSocket,
    idea_id: uuid.UUID,
    session: AsyncSession = Depends(get_session),
):
    await vote_manager.connect(websocket, idea_id)
    try:
        # Send initial vote counts
        initial_counts = await idea_service.get_vote_counts(idea_id, session)
        await websocket.send_json(initial_counts)

        # Keep connection alive and handle any client messages
        while True:
            try:
                await websocket.receive_text()  # Heartbeat or other client messages
            except WebSocketDisconnect:
                vote_manager.disconnect(websocket, idea_id)
                break
    except Exception as e:
        vote_manager.disconnect(websocket, idea_id)
        raise


@idea_router.post("/ideas/{idea_id}/votes")
async def vote(
    idea_id: uuid.UUID,
    vote_data: VoteCreationModel,
    token: dict = Depends(AccessTokenBearer()),
    session: AsyncSession = Depends(get_session),
):

    # Handle the vote
    try:
        await idea_service.handle_vote(
            idea_id, token["user"]["user_id"], vote_data, session
        )

        # Get updated vote counts
        updated_counts = await idea_service.get_vote_counts(idea_id, session)

        # Broadcast update to all connected clients
        await vote_manager.broadcast_vote_update(idea_id, updated_counts)

        return updated_counts
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@idea_router.get("/ideas/{idea_id}/votes")
async def get_votes(idea_id: uuid.UUID, session: AsyncSession = Depends(get_session)):
    return await idea_service.get_vote_counts(idea_id, session)


@idea_router.delete("/ideas/{idea_id}/votes")
async def remove_vote(
    idea_id: uuid.UUID,
    session: AsyncSession = Depends(get_session),
    token: dict = Depends(AccessTokenBearer()),
):
    try:
        await idea_service.delete_vote(idea_id, token["user"]["user_id"], session)
        updated_counts = await idea_service.get_vote_counts(idea_id, session)
        await vote_manager.broadcast_vote_update(idea_id, updated_counts)
        return updated_counts
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
