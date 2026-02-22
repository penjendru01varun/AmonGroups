import uuid
from datetime import datetime
from typing import Dict, Any, List, Optional
from enum import Enum


class AgentState(str, Enum):
    IDLE = "idle"
    PROCESSING = "processing"
    WAITING = "waiting"
    ALERT = "alert"
    ERROR = "error"
    DEAD = "dead"


class BaseAgent:
    """Base class for all agents in the MAITRI system"""

    def __init__(
        self,
        agent_id: str = None,
        name: str = "BaseAgent",
        agent_type: str = "general",
        capabilities: List[str] = None,
        dependencies: List[str] = None,
    ):
        self.agent_id = agent_id or f"agent_{uuid.uuid4().hex[:8]}"
        self.name = name
        self.agent_type = agent_type
        self.capabilities = capabilities or []
        self.dependencies = dependencies or []
        
        self.state = AgentState.IDLE
        self.status_message = "Initialized"
        
        self.memory = {
            "short_term": [],
            "long_term": [],
        }
        
        self.performance_metrics = {
            "tasks_processed": 0,
            "avg_response_time": 0,
            "error_rate": 0,
            "last_heartbeat": datetime.now().isoformat(),
        }
        
        self.message_history = []
        
    def update_status(self, status: str, message: str = ""):
        """Update agent status"""
        try:
            self.state = AgentState(status)
        except ValueError:
            self.state = AgentState.IDLE
        if message:
            self.status_message = message

    def add_to_memory(self, key: str, value: Any):
        """Add interaction to memory"""
        self.memory["short_term"].append({
            "timestamp": datetime.now().isoformat(),
            "data": value,
        })
        
        if len(self.memory["short_term"]) > 100:
            self.memory["short_term"].pop(0)

    def log_activity(self, message: str):
        """Log agent activity"""
        self.message_history.append({
            "timestamp": datetime.now().isoformat(),
            "message": message,
            "agent": self.name,
        })
        
        if len(self.message_history) > 50:
            self.message_history.pop(0)

    async def process(self, input_data: Dict[str, Any]) -> Dict[str, Any]:
        """Process input data - to be implemented by subclasses"""
        raise NotImplementedError("Subclasses must implement process()")

    async def receive_message(self, message: Dict[str, Any]) -> Dict[str, Any]:
        """Receive and process a message"""
        self.update_status("processing")
        self.performance_metrics["tasks_processed"] += 1
        
        result = await self.process(message.get("payload", {}))
        
        self.update_status("idle")
        return result

    async def send_message(self, target_agent: str, payload: Dict[str, Any]):
        """Send message to another agent via message bus"""
        from ..core.message_bus import message_bus
        
        message = {
            "message_id": str(uuid.uuid4()),
            "type": "task",
            "source_agent": self.agent_id,
            "target_agent": target_agent,
            "priority": 5,
            "timestamp": datetime.now().isoformat(),
            "payload": payload,
            "requires_response": False,
            "correlation_id": None,
        }
        
        await message_bus.publish(message)

    def get_status(self) -> Dict[str, Any]:
        """Get current agent status"""
        return {
            "agent_id": self.agent_id,
            "name": self.name,
            "type": self.agent_type,
            "state": self.state.value,
            "status_message": self.status_message,
            "capabilities": self.capabilities,
            "metrics": self.performance_metrics,
        }

    async def heartbeat(self):
        """Send heartbeat to orchestrator"""
        self.performance_metrics["last_heartbeat"] = datetime.now().isoformat()
