import asyncio
import json
import uuid
from datetime import datetime
from typing import Dict, Any, List, Callable, Optional
from collections import defaultdict
from dataclasses import dataclass, field


@dataclass
class Message:
    message_id: str = field(default_factory=lambda: str(uuid.uuid4()))
    type: str = "task"
    source_agent: str = ""
    target_agent: str = ""
    priority: int = 5
    timestamp: str = field(default_factory=lambda: datetime.now().isoformat())
    payload: Dict[str, Any] = field(default_factory=dict)
    requires_response: bool = False
    correlation_id: Optional[str] = None


class MessageBus:
    """Message bus for inter-agent communication"""
    
    def __init__(self):
        self.subscribers: Dict[str, List[Callable]] = defaultdict(list)
        self.message_history: List[Message] = []
        self.pending_responses: Dict[str, asyncio.Future] = {}
        
    def subscribe(self, agent_id: str, callback: Callable):
        """Subscribe to messages for a specific agent"""
        self.subscribers[agent_id].append(callback)
        
    def unsubscribe(self, agent_id: str, callback: Callable):
        """Unsubscribe from messages"""
        if agent_id in self.subscribers:
            self.subscribers[agent_id].remove(callback)
            
    async def publish(self, message: Dict[str, Any]):
        """Publish message to the bus"""
        msg = Message(**message)
        
        self.message_history.append(msg)
        
        if len(self.message_history) > 1000:
            self.message_history.pop(0)
        
        target = msg.target_agent
        
        if target and target in self.subscribers:
            for callback in self.subscribers[target]:
                try:
                    if asyncio.iscoroutinefunction(callback):
                        await callback(msg)
                    else:
                        callback(msg)
                except Exception as e:
                    print(f"Error in subscriber callback: {e}")
        
        if msg.requires_response and msg.correlation_id:
            if msg.correlation_id in self.pending_responses:
                self.pending_responses[msg.correlation_id].set_result(msg)
                
    async def request_response(self, message: Dict[str, Any], timeout: float = 5.0) -> Message:
        """Send message and wait for response"""
        correlation_id = str(uuid.uuid4())
        message["correlation_id"] = correlation_id
        message["requires_response"] = True
        
        future = asyncio.Future()
        self.pending_responses[correlation_id] = future
        
        await self.publish(message)
        
        try:
            result = await asyncio.wait_for(future, timeout=timeout)
            return result
        except asyncio.TimeoutError:
            raise TimeoutError(f"Message {correlation_id} timed out after {timeout}s")
        finally:
            del self.pending_responses[correlation_id]
            
    def get_messages_for_agent(self, agent_id: str, limit: int = 50) -> List[Message]:
        """Get message history for specific agent"""
        messages = [
            m for m in self.message_history
            if m.target_agent == agent_id or m.source_agent == agent_id
        ]
        return messages[-limit:]
    
    def clear_history(self):
        """Clear message history"""
        self.message_history.clear()


message_bus = MessageBus()
