import asyncio
import json
from typing import Dict, Set
from collections import defaultdict
from fastapi import WebSocket
import uuid


class WebSocketManager:
    """Manages WebSocket connections and broadcasting"""
    
    def __init__(self):
        self.active_connections: Dict[str, WebSocket] = {}
        self.subscriptions: Dict[str, Set[str]] = defaultdict(set)
        
    async def connect(self, websocket: WebSocket, client_id: str = None):
        """Connect a new WebSocket client"""
        await websocket.accept()
        
        if client_id is None:
            client_id = str(uuid.uuid4())
            
        self.active_connections[client_id] = websocket
        
        return client_id
    
    def disconnect(self, client_id: str):
        """Disconnect a WebSocket client"""
        if client_id in self.active_connections:
            del self.active_connections[client_id]
            
        for topic in self.subscriptions:
            self.subscriptions[topic].discard(client_id)
    
    async def send_personal_message(self, message: Dict, client_id: str):
        """Send message to specific client"""
        if client_id in self.active_connections:
            websocket = self.active_connections[client_id]
            try:
                await websocket.send_json(message)
            except Exception as e:
                print(f"Error sending message to {client_id}: {e}")
                
    async def broadcast(self, message: Dict):
        """Broadcast message to all connected clients"""
        disconnected = []
        
        for client_id, websocket in self.active_connections.items():
            try:
                await websocket.send_json(message)
            except Exception as e:
                print(f"Error broadcasting to {client_id}: {e}")
                disconnected.append(client_id)
                
        for client_id in disconnected:
            self.disconnect(client_id)
    
    async def broadcast_to_topic(self, message: Dict, topic: str):
        """Broadcast message to clients subscribed to topic"""
        if topic not in self.subscriptions:
            return
            
        disconnected = []
        
        for client_id in self.subscriptions[topic]:
            if client_id in self.active_connections:
                try:
                    await self.active_connections[client_id].send_json(message)
                except Exception as e:
                    print(f"Error sending to {client_id}: {e}")
                    disconnected.append(client_id)
        
        for client_id in disconnected:
            self.subscriptions[topic].discard(client_id)
    
    def subscribe(self, client_id: str, topic: str):
        """Subscribe client to topic"""
        self.subscriptions[topic].add(client_id)
    
    def unsubscribe(self, client_id: str, topic: str):
        """Unsubscribe client from topic"""
        self.subscriptions[topic].discard(client_id)
    
    def get_connection_count(self) -> int:
        """Get number of active connections"""
        return len(self.active_connections)
    
    async def receive_json(self, websocket: WebSocket) -> Dict:
        """Receive JSON from WebSocket"""
        try:
            data = await websocket.receive_json()
            return data
        except Exception as e:
            print(f"Error receiving JSON: {e}")
            return {}


ws_manager = WebSocketManager()
