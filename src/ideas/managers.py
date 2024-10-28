from typing import Dict, Set, Optional
from fastapi import WebSocket, WebSocketDisconnect
import uuid


# WebSocket connection manager
class VoteConnectionManager:
    def __init__(self):
        # Dictionary of idea_id to set of WebSocket connections
        self.active_connections: Dict[uuid.UUID, Set[WebSocket]] = {}

    async def connect(self, websocket: WebSocket, idea_id: uuid.UUID):
        await websocket.accept()
        if idea_id not in self.active_connections:
            self.active_connections[idea_id] = set()
        self.active_connections[idea_id].add(websocket)

    def disconnect(self, websocket: WebSocket, idea_id: uuid.UUID):
        self.active_connections[idea_id].remove(websocket)
        if not self.active_connections[idea_id]:
            del self.active_connections[idea_id]

    async def broadcast_vote_update(self, idea_id: uuid.UUID, vote_data: dict):
        if idea_id in self.active_connections:
            dead_connections = set()
            for connection in self.active_connections[idea_id]:
                try:
                    await connection.send_json(vote_data)
                except WebSocketDisconnect:
                    dead_connections.add(connection)

            # Clean up dead connections
            for dead_connection in dead_connections:
                self.disconnect(dead_connection, idea_id)
