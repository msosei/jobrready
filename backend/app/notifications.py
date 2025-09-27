"""
Real-time Notification System for MyBrand Job Application Platform
Version: v2
Purpose: Provides WebSocket-based real-time notifications and messaging
"""

# ============================================================================
# IMPORT STATEMENTS
# Standard library and third-party imports for notification functionality
# ============================================================================

from fastapi import APIRouter, WebSocket, WebSocketDisconnect
from typing import List, Dict
import json
import asyncio
from datetime import datetime
import uuid
import logging

# ============================================================================
# LOGGING CONFIGURATION
# Set up logging for monitoring and debugging notification events
# ============================================================================

logger = logging.getLogger(__name__)

# ============================================================================
# CONNECTION MANAGER CLASS
# Manages WebSocket connections and message distribution to clients
# ============================================================================

class ConnectionManager:
    """
    Manages WebSocket connections and facilitates real-time message distribution.
    
    This class maintains active connections and provides methods for sending
    messages to individual users or broadcasting to all connected clients.
    It handles connection lifecycle events and automatic cleanup of
    disconnected clients.
    """
    
    def __init__(self):
        """
        Initialize the ConnectionManager with empty connection tracking structures.
        """
        # Track active WebSocket connections by connection ID
        self.active_connections: Dict[str, WebSocket] = {}
        
        # Map user IDs to their connection IDs for targeted messaging
        self.user_connections: Dict[str, List[str]] = {}  # user_id -> list of connection_ids

    async def connect(self, websocket: WebSocket, user_id: str = "anonymous"):
        """
        Establish a new WebSocket connection and register it with the manager.
        
        Args:
            websocket (WebSocket): The WebSocket connection to register
            user_id (str): Identifier for the user (defaults to "anonymous")
            
        Returns:
            str: Unique connection ID for the newly established connection
        """
        # Accept the WebSocket connection
        await websocket.accept()
        
        # Generate a unique identifier for this connection
        connection_id = str(uuid.uuid4())
        
        # Register the connection in our tracking structures
        self.active_connections[connection_id] = websocket
        
        # Associate the connection with the user
        if user_id not in self.user_connections:
            self.user_connections[user_id] = []
        self.user_connections[user_id].append(connection_id)
        
        # Send welcome message to confirm connection
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
        """
        Clean up and remove a disconnected WebSocket connection.
        
        Args:
            connection_id (str): The unique identifier of the connection to remove
            user_id (str): The user ID associated with the connection
        """
        # Remove the connection from active connections
        if connection_id in self.active_connections:
            del self.active_connections[connection_id]
        
        # Remove the connection from user associations
        if user_id in self.user_connections:
            if connection_id in self.user_connections[user_id]:
                self.user_connections[user_id].remove(connection_id)
            # Clean up empty user connection lists
            if not self.user_connections[user_id]:
                del self.user_connections[user_id]

    async def send_personal_message(self, message: dict, connection_id: str):
        """
        Send a message to a specific WebSocket connection.
        
        Args:
            message (dict): The message payload to send
            connection_id (str): The unique identifier of the target connection
        """
        # Verify the connection exists before sending
        if connection_id in self.active_connections:
            try:
                # Send the message as JSON
                await self.active_connections[connection_id].send_text(json.dumps(message))
            except WebSocketDisconnect:
                # Handle disconnected clients gracefully
                logger.info(f"WebSocket disconnected for connection {connection_id}")
                # Clean up the disconnected connection
                user_id = None
                for uid, connections in self.user_connections.items():
                    if connection_id in connections:
                        user_id = uid
                        break
                self.disconnect(connection_id, user_id or "anonymous")
            except Exception as e:
                # Log any other errors during message sending
                logger.error(f"Error sending message to connection {connection_id}: {e}")

    async def send_to_user(self, message: dict, user_id: str):
        """
        Send a message to all connections associated with a specific user.
        
        Args:
            message (dict): The message payload to send
            user_id (str): The identifier of the target user
        """
        # Verify the user has active connections
        if user_id in self.user_connections:
            # Track any connections that become disconnected during sending
            disconnected_connections = []
            
            # Send message to all connections for this user
            for connection_id in self.user_connections[user_id]:
                try:
                    await self.send_personal_message(message, connection_id)
                except Exception as e:
                    logger.error(f"Error sending message to user {user_id}: {e}")
                    disconnected_connections.append(connection_id)
            
            # Clean up any connections that became disconnected
            for connection_id in disconnected_connections:
                self.disconnect(connection_id, user_id)

    async def broadcast(self, message: dict):
        """
        Send a message to all currently connected WebSocket clients.
        
        Args:
            message (dict): The message payload to broadcast to all clients
        """
        # Track connections that become disconnected during broadcasting
        disconnected_connections = []
        
        # Send message to all active connections
        for connection_id, websocket in self.active_connections.items():
            try:
                await websocket.send_text(json.dumps(message))
            except WebSocketDisconnect:
                disconnected_connections.append(connection_id)
            except Exception as e:
                logger.error(f"Error broadcasting message to connection {connection_id}: {e}")
                disconnected_connections.append(connection_id)
        
        # Clean up all disconnected connections
        for connection_id in disconnected_connections:
            # Find the user ID for this connection
            user_id = None
            for uid, connections in self.user_connections.items():
                if connection_id in connections:
                    user_id = uid
                    break
            self.disconnect(connection_id, user_id or "anonymous")

# ============================================================================
# SINGLETON INSTANCE
# Create a single instance of ConnectionManager for the application
# ============================================================================

manager = ConnectionManager()

# ============================================================================
# ROUTER CONFIGURATION
# Create router for notification endpoints with appropriate tags
# ============================================================================

router = APIRouter(tags=["Notifications"])

# ============================================================================
# WEBSOCKET ENDPOINTS
# Real-time communication endpoints for notifications
# ============================================================================

@router.websocket("/ws/notifications")
async def websocket_endpoint(websocket: WebSocket, user_id: str = "anonymous"):
    """
    WebSocket endpoint for real-time notification delivery.
    
    Maintains a persistent connection with clients to deliver real-time
    notifications. Sends periodic keepalive messages to maintain connection.
    
    Args:
        websocket (WebSocket): The WebSocket connection from the client
        user_id (str): Identifier for the connecting user (defaults to "anonymous")
    """
    # Establish the WebSocket connection
    connection_id = await manager.connect(websocket, user_id)
    
    try:
        # Maintain connection with periodic keepalive messages
        while True:
            # Send keepalive every 30 seconds to maintain connection
            await asyncio.sleep(30)
            await manager.send_personal_message({
                "id": f"keepalive-{uuid.uuid4()}",
                "type": "job_match",
                "title": "Keep Alive",
                "message": "Connection maintained",
                "timestamp": datetime.now().isoformat(),
                "read": True
            }, connection_id)
    except WebSocketDisconnect:
        # Handle normal WebSocket disconnection
        logger.info(f"WebSocket disconnected for user {user_id}")
        manager.disconnect(connection_id, user_id)
    except Exception as e:
        # Handle unexpected errors in the WebSocket connection
        logger.error(f"Unexpected error in WebSocket connection for user {user_id}: {e}")
        manager.disconnect(connection_id, user_id)

# ============================================================================
# HTTP ENDPOINTS
# RESTful endpoints for sending notifications
# ============================================================================

@router.post("/notifications/send")
async def send_notification(
    user_id: str = "anonymous",
    notification_type: str = "job_match",
    title: str = "Notification",
    message: str = "You have a new notification",
    data: dict | None = None
):
    """
    Send a notification to a specific user or broadcast to all users.
    
    Creates and delivers a notification message to the specified user
    or broadcasts it to all connected clients if no user is specified.
    
    Args:
        user_id (str): Target user ID (defaults to "anonymous" for broadcast)
        notification_type (str): Category/type of notification
        title (str): Title/subject of the notification
        message (str): Main content of the notification
        data (dict, optional): Additional structured data to include
        
    Returns:
        dict: Confirmation of successful notification delivery
    """
    # Create the notification payload with standardized structure
    notification = {
        "id": f"{notification_type}-{uuid.uuid4()}",
        "type": notification_type,
        "title": title,
        "message": message,
        "data": data or {},
        "timestamp": datetime.now().isoformat(),
        "read": False
    }
    
    # Deliver the notification to the appropriate recipient(s)
    if user_id != "anonymous":
        # Send to specific user
        await manager.send_to_user(notification, user_id)
    else:
        # Broadcast to all connected clients
        await manager.broadcast(notification)
    
    # Return success confirmation
    return {"success": True}