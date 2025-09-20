from fastapi import APIRouter, WebSocket, WebSocketDisconnect
from typing import List, Dict
import json
import asyncio
from datetime import datetime
import uuid

class ConnectionManager:
    def __init__(self):
        self.active_connections: Dict[str, WebSocket] = {}
        self.user_connections: Dict[str, List[str]] = {}  # user_id -> list of connection_ids

    async def connect(self, websocket: WebSocket, user_id: str = "anonymous"):
        await websocket.accept()
        connection_id = str(uuid.uuid4())
        self.active_connections[connection_id] = websocket
        
        if user_id not in self.user_connections:
            self.user_connections[user_id] = []
        self.user_connections[user_id].append(connection_id)
        
        # Send welcome message
        await self.send_personal_message({
            "id": f"welcome-{uuid.uuid4()}",
            "type": "job_match",
            "title": "Welcome!",
            "message": "You are now connected to real-time notifications",
            "timestamp": datetime.now().isoformat(),
            "read": False
        }, connection_id)
        
        return connection_id

    def disconnect(self, connection_id: str, user_id: str = "anonymous"):
        if connection_id in self.active_connections:
            del self.active_connections[connection_id]
        
        if user_id in self.user_connections:
            if connection_id in self.user_connections[user_id]:
                self.user_connections[user_id].remove(connection_id)
            if not self.user_connections[user_id]:  # Clean up empty lists
                del self.user_connections[user_id]

    async def send_personal_message(self, message: dict, connection_id: str):
        if connection_id in self.active_connections:
            try:
                await self.active_connections[connection_id].send_text(json.dumps(message))
            except WebSocketDisconnect:
                pass  # Connection already closed

    async def send_to_user(self, message: dict, user_id: str):
        if user_id in self.user_connections:
            # Send to all connections for this user
            for connection_id in self.user_connections[user_id]:
                await self.send_personal_message(message, connection_id)

    async def broadcast(self, message: dict):
        # Send to all connected clients
        disconnected_connections = []
        for connection_id, websocket in self.active_connections.items():
            try:
                await websocket.send_text(json.dumps(message))
            except WebSocketDisconnect:
                disconnected_connections.append(connection_id)
        
        # Clean up disconnected connections
        for connection_id in disconnected_connections:
            # Find the user_id for this connection
            user_id = None
            for uid, connections in self.user_connections.items():
                if connection_id in connections:
                    user_id = uid
                    break
            self.disconnect(connection_id, user_id or "anonymous")

# Create a single instance of ConnectionManager
manager = ConnectionManager()

# Create router for notification endpoints
router = APIRouter()

@router.websocket("/ws/notifications")
async def websocket_endpoint(websocket: WebSocket, user_id: str = "anonymous"):
    connection_id = await manager.connect(websocket, user_id)
    try:
        while True:
            # Keep the connection alive
            await asyncio.sleep(30)  # Send keepalive every 30 seconds
            await manager.send_personal_message({
                "id": f"keepalive-{uuid.uuid4()}",
                "type": "job_match",
                "title": "Keep Alive",
                "message": "Connection maintained",
                "timestamp": datetime.now().isoformat(),
                "read": True
            }, connection_id)
    except WebSocketDisconnect:
        manager.disconnect(connection_id, user_id)

@router.post("/notifications/send")
async def send_notification(
    user_id: str = "anonymous",
    notification_type: str = "job_match",
    title: str = "Notification",
    message: str = "You have a new notification",
    data: dict | None = None
):
    notification = {
        "id": f"{notification_type}-{uuid.uuid4()}",
        "type": notification_type,
        "title": title,
        "message": message,
        "data": data or {},
        "timestamp": datetime.now().isoformat(),
        "read": False
    }
    
    if user_id != "anonymous":
        await manager.send_to_user(notification, user_id)
    else:
        await manager.broadcast(notification)
    
    return {"success": True}
