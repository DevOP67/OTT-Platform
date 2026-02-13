from fastapi import WebSocket, WebSocketDisconnect
from typing import Dict, List, Set
import json
import logging
from datetime import datetime, timezone

logger = logging.getLogger(__name__)

class ConnectionManager:
    """Manages WebSocket connections for group watch sessions"""
    
    def __init__(self):
        # session_id -> set of websocket connections
        self.active_connections: Dict[str, Set[WebSocket]] = {}
        # session_id -> playback state
        self.session_states: Dict[str, Dict] = {}
    
    async def connect(self, websocket: WebSocket, session_id: str, user_id: str):
        """Connect a user to a group session"""
        await websocket.accept()
        
        if session_id not in self.active_connections:
            self.active_connections[session_id] = set()
        
        self.active_connections[session_id].add(websocket)
        
        # Send current state to new user
        if session_id in self.session_states:
            await websocket.send_json({
                'type': 'state_sync',
                'state': self.session_states[session_id]
            })
        
        # Notify others
        await self.broadcast(session_id, {
            'type': 'user_joined',
            'user_id': user_id,
            'timestamp': datetime.now(timezone.utc).isoformat()
        }, exclude=websocket)
        
        logger.info(f"User {user_id} connected to session {session_id}")
    
    def disconnect(self, websocket: WebSocket, session_id: str, user_id: str):
        """Disconnect a user from a group session"""
        if session_id in self.active_connections:
            self.active_connections[session_id].discard(websocket)
            
            # Clean up empty sessions
            if not self.active_connections[session_id]:
                del self.active_connections[session_id]
                if session_id in self.session_states:
                    del self.session_states[session_id]
        
        logger.info(f"User {user_id} disconnected from session {session_id}")
    
    async def broadcast(self, session_id: str, message: dict, exclude: WebSocket = None):
        """Broadcast message to all users in a session"""
        if session_id not in self.active_connections:
            return
        
        disconnected = set()
        for connection in self.active_connections[session_id]:
            if connection == exclude:
                continue
            
            try:
                await connection.send_json(message)
            except Exception as e:
                logger.error(f"Error broadcasting to connection: {e}")
                disconnected.add(connection)
        
        # Remove disconnected connections
        for conn in disconnected:
            self.active_connections[session_id].discard(conn)
    
    async def update_playback_state(self, session_id: str, state: dict, websocket: WebSocket):
        """Update and sync playback state across all users"""
        self.session_states[session_id] = state
        
        await self.broadcast(session_id, {
            'type': 'playback_update',
            'state': state,
            'timestamp': datetime.now(timezone.utc).isoformat()
        }, exclude=websocket)
    
    async def send_message(self, session_id: str, user_id: str, message: str, websocket: WebSocket):
        """Send chat message to all users in session"""
        await self.broadcast(session_id, {
            'type': 'chat_message',
            'user_id': user_id,
            'message': message,
            'timestamp': datetime.now(timezone.utc).isoformat()
        }, exclude=websocket)

# Global manager instance
manager = ConnectionManager()
