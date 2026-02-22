import uuid
import asyncio
from datetime import datetime
from typing import Dict, Any, List, Optional
from collections import deque
import networkx as nx
from .base_agent import BaseAgent, AgentState


class OrchestratorAgent(BaseAgent):
    """Master orchestrator that manages all agent coordination"""

    def __init__(self, agent_id: str = None):
        super().__init__(
            agent_id=agent_id or "orchestrator",
            name="Orchestrator",
            agent_type="core",
            capabilities=[
                "task_delegation",
                "workflow_orchestration",
                "agent_lifecycle_management",
                "conflict_resolution",
                "priority_scheduling",
            ],
        )
        
        self.registered_agents: Dict[str, BaseAgent] = {}
        self.task_queue = asyncio.PriorityQueue()
        self.active_tasks: Dict[str, Dict] = {}
        self.task_history = deque(maxlen=1000)
        self.workflow_graph = nx.DiGraph()
        self.agent_performance: Dict[str, Dict] = {}
        
        self.agent_mapping = {
            "vitals_check": "vitals_agent",
            "exercise_recommendation": "exercise_agent",
            "sleep_analysis": "sleep_agent",
            "meal_plan": "nutrition_agent",
            "counseling": "counselor_agent",
            "mood_detection": "mood_agent",
            "social_check": "social_agent",
            "alert": "alert_agent",
            "simulation": "digital_twin",
            "health_prediction": "digital_twin",
            "get_status": "orchestrator",
        }

    async def register_agent(self, agent: BaseAgent):
        """Register a new agent with the orchestrator"""
        self.registered_agents[agent.agent_id] = agent
        
        self.workflow_graph.add_node(agent.agent_id, name=agent.name, type=agent.agent_type)
        
        self.agent_performance[agent.agent_id] = {
            "tasks_processed": 0,
            "avg_response_time": 0,
            "error_rate": 0,
            "queue_size": 0,
            "last_heartbeat": datetime.now().isoformat(),
        }
        
        self.log_activity(f"Registered agent: {agent.name} ({agent.agent_id})")

    async def process(self, input_data: Dict[str, Any]) -> Dict[str, Any]:
        """Process orchestration request"""
        self.update_status("processing")
        
        action = input_data.get("action", "delegate_task")
        
        if action == "delegate_task":
            result = await self._delegate_task(input_data.get("task", {}))
        elif action == "get_system_status":
            result = await self._get_system_status()
        elif action == "handle_complex_query":
            result = await self._handle_complex_query(input_data)
        elif action == "get_agent_info":
            result = await self._get_agent_info(input_data.get("agent_id"))
        else:
            result = {
                "agent": self.name,
                "error": f"Unknown action: {action}",
                "timestamp": datetime.now().isoformat(),
            }
        
        self.update_status("idle")
        return result

    async def _delegate_task(self, task: Dict) -> Dict:
        """Delegate task to appropriate agent using mapping"""
        task_id = task.get("id", f"task_{uuid.uuid4().hex[:8]}")
        task_type = task.get("type", "unknown")
        task_priority = task.get("priority", 5)
        
        target_agent_id = self.agent_mapping.get(task_type)
        
        if not target_agent_id or target_agent_id not in self.registered_agents:
            return {
                "task_id": task_id,
                "status": "failed",
                "error": f"No suitable agent for task type: {task_type}",
                "timestamp": datetime.now().isoformat(),
            }
        
        target_agent = self.registered_agents[target_agent_id]
        
        task_data = task.get("data", {})
        
        try:
            result = await target_agent.process(task_data)
            
            self.active_tasks[task_id] = {
                "task": task,
                "target_agent": target_agent_id,
                "status": "completed",
                "completed_at": datetime.now().isoformat(),
            }
            
            self.task_history.append({
                "task_id": task_id,
                "type": task_type,
                "agent": target_agent_id,
                "status": "completed",
                "completed_at": datetime.now().isoformat(),
            })
            
            if target_agent_id in self.agent_performance:
                self.agent_performance[target_agent_id]["tasks_processed"] += 1
            
            self.log_activity(f"Task {task_id} completed by {target_agent.name}")
            
            return {
                "task_id": task_id,
                "status": "completed",
                "agent": target_agent.name,
                "result": result,
                "timestamp": datetime.now().isoformat(),
            }
            
        except Exception as e:
            return {
                "task_id": task_id,
                "status": "failed",
                "error": str(e),
                "timestamp": datetime.now().isoformat(),
            }

    async def _get_system_status(self) -> Dict:
        """Get overall system status"""
        agent_states = {}
        
        for agent_id, agent in self.registered_agents.items():
            agent_states[agent_id] = {
                "name": agent.name,
                "type": agent.agent_type,
                "state": agent.state.value,
                "status_message": agent.status_message,
                "capabilities": agent.capabilities,
            }
        
        return {
            "agent": self.name,
            "total_agents": len(self.registered_agents),
            "agents": agent_states,
            "tasks_in_queue": self.task_queue.qsize(),
            "active_tasks": len(self.active_tasks),
            "completed_tasks": len(self.task_history),
            "workflow_complexity": self.workflow_graph.number_of_edges(),
            "timestamp": datetime.now().isoformat(),
        }

    async def _handle_complex_query(self, input_data: Dict) -> Dict:
        """Handle complex queries requiring multiple agents"""
        query = input_data.get("query", "")
        
        dag_result = {
            "query": query,
            "tasks": [],
            "results": {},
            "synthesized_response": "",
        }
        
        query_lower = query.lower()
        
        if any(word in query_lower for word in ["anxious", "stress", "worried", "feeling"]):
            dag_result["tasks"].append({
                "type": "mood_detection",
                "agent": "mood_agent",
                "status": "pending",
            })
            dag_result["tasks"].append({
                "type": "counseling",
                "agent": "counselor_agent",
                "status": "pending",
            })
        
        if any(word in query_lower for word in ["heart", "tired", "sick"]):
            dag_result["tasks"].append({
                "type": "vitals_check",
                "agent": "vitals_agent",
                "status": "pending",
            })
        
        if not dag_result["tasks"]:
            dag_result["tasks"].append({
                "type": "get_status",
                "agent": "orchestrator",
                "status": "pending",
            })
        
        for task in dag_result["tasks"]:
            task_result = await self._delegate_task({
                "id": f"subtask_{task['agent']}",
                "type": task["type"],
                "data": {"query": query},
            })
            task["status"] = "completed"
            dag_result["results"][task["agent"]] = task_result
        
        dag_result["synthesized_response"] = self._synthesize_response(dag_result["results"])
        
        return {
            "agent": self.name,
            "dag_result": dag_result,
            "timestamp": datetime.now().isoformat(),
        }

    def _synthesize_response(self, results: Dict) -> str:
        """Synthesize response from multiple agent results"""
        responses = []
        
        for agent_id, result in results.items():
            if isinstance(result, dict) and "result" in result:
                res = result["result"]
                if isinstance(res, dict):
                    if "response" in res:
                        responses.append(res["response"])
                    elif "mood_analysis" in res:
                        analysis = res["mood_analysis"]
                        responses.append(f"Mood detected: {analysis.get('emotion', 'unknown')}")
        
        if responses:
            return " ".join(responses[:2])
        
        return "I've analyzed your request. How can I help you further?"

    async def _get_agent_info(self, agent_id: str) -> Dict:
        """Get specific agent information"""
        if agent_id not in self.registered_agents:
            return {
                "error": f"Agent {agent_id} not found",
                "timestamp": datetime.now().isoformat(),
            }
        
        agent = self.registered_agents[agent_id]
        
        return {
            "agent_id": agent.agent_id,
            "name": agent.name,
            "type": agent.agent_type,
            "state": agent.state.value,
            "status_message": agent.status_message,
            "capabilities": agent.capabilities,
            "dependencies": agent.dependencies,
            "metrics": agent.performance_metrics,
            "timestamp": datetime.now().isoformat(),
        }
