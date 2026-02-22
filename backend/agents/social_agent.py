import random
from datetime import datetime
from typing import Dict, Any, List
from .base_agent import BaseAgent


class SocialAgent(BaseAgent):
    """Manages crew communication and morale"""

    def __init__(self, agent_id: str = None):
        super().__init__(
            agent_id=agent_id or "social_agent",
            name="Social Agent",
            agent_type="psychological",
            capabilities=[
                "crew_communication",
                "morale_tracking",
                "team_dynamics",
                "family_connections",
            ],
        )
        
        self.crew_members = [
            {"name": "Commander Sharma", "role": "Commander", "status": "active"},
            {"name": "Dr. Chen", "role": "Mission Specialist", "status": "active"},
            {"name": "Engineer Kowalski", "role": "Flight Engineer", "status": "active"},
        ]
        
        self.morale_events = []
        self.communications = []

    async def process(self, input_data: Dict[str, Any]) -> Dict[str, Any]:
        """Process social request"""
        action = input_data.get("action", "get_status")
        
        if action == "get_status":
            return await self._get_status()
        elif action == "send_message":
            return await self._send_message(input_data)
        elif action == "get_morale":
            return await self._get_morale()
        elif action == "schedule_activity":
            return await self._schedule_activity(input_data)
        elif action == "family_call":
            return await self._family_call(input_data)
        else:
            return {"error": f"Unknown action: {action}"}

    async def _get_status(self) -> Dict[str, Any]:
        """Get crew and social status"""
        return {
            "agent": self.name,
            "crew_status": self.crew_members,
            "active_conversations": len([c for c in self.communications if c.get("active")]),
            "timestamp": datetime.now().isoformat(),
        }

    async def _send_message(self, data: Dict) -> Dict[str, Any]:
        """Send message to crew member"""
        recipient = data.get("recipient")
        message = data.get("message", "")
        priority = data.get("priority", "normal")
        
        communication = {
            "id": str(random.randint(1000, 9999)),
            "from": "Astronaut",
            "to": recipient,
            "message": message,
            "priority": priority,
            "timestamp": datetime.now().isoformat(),
            "delivered": True,
            "read": False,
        }
        
        self.communications.append(communication)
        
        return {
            "agent": self.name,
            "communication": communication,
            "status": "sent",
            "timestamp": datetime.now().isoformat(),
        }

    async def _get_morale(self) -> Dict[str, Any]:
        """Get current crew morale status"""
        morale_score = random.randint(70, 95)
        
        morale_factors = {
            "team_cohesion": random.randint(70, 95),
            "communication_quality": random.randint(65, 90),
            "shared_activities": random.randint(50, 85),
            "personal_satisfaction": random.randint(65, 95),
        }
        
        trends = []
        if morale_score > 85:
            trends.append("Crew is thriving")
            trends.append("Strong team bonding")
        elif morale_score > 70:
            trends.append("Crew is doing well")
            trends.append("Normal mission operations")
        else:
            trends.append("Consider team activities")
            trends.append("Monitor for conflicts")
        
        return {
            "agent": self.name,
            "morale_score": morale_score,
            "factors": morale_factors,
            "trends": trends,
            "recommendations": self._get_morale_recommendations(morale_score),
            "timestamp": datetime.now().isoformat(),
        }

    def _get_morale_recommendations(self, score: int) -> List[str]:
        """Get morale improvement recommendations"""
        if score < 60:
            return [
                "Schedule team movie night",
                "Organize virtual game session",
                "Plan special meal together",
                "Connect with mission control for morale boost",
            ]
        elif score < 80:
            return [
                "Encourage informal crew hangouts",
                "Share personal stories and hobbies",
                "Rotate meal preparation duties",
            ]
        else:
            return [
                "Maintain current team dynamics",
                "Consider mentoring new crew",
                "Share success stories with Earth",
            ]

    async def _schedule_activity(self, data: Dict) -> Dict[str, Any]:
        """Schedule team activity"""
        activity_type = data.get("type", "social")
        participants = data.get("participants", "all")
        
        activities = {
            "exercise": "Group workout session",
            "meal": "Shared meal with conversation",
            "game": "Virtual game tournament",
            "movie": "Movie night in common area",
            "conversation": "Team check-in meeting",
            "training": "Joint training exercise",
        }
        
        activity = {
            "id": str(random.randint(1000, 9999)),
            "type": activity_type,
            "name": activities.get(activity_type, "Team activity"),
            "participants": participants,
            "scheduled_time": data.get("time", "19:00"),
            "duration_minutes": data.get("duration", 60),
            "created_at": datetime.now().isoformat(),
        }
        
        return {
            "agent": self.name,
            "activity": activity,
            "status": "scheduled",
            "timestamp": datetime.now().isoformat(),
        }

    async def _family_call(self, data: Dict) -> Dict[str, Any]:
        """Schedule family video call"""
        family_member = data.get("family_member", "Family")
        duration = data.get("duration", 15)
        
        available_slots = ["08:00", "12:00", "19:00", "21:00"]
        
        call_request = {
            "id": str(random.randint(1000, 9999)),
            "type": "family_video",
            "with": family_member,
            "requested_duration": duration,
            "available_slots": available_slots,
            "priority": "high",
            "bandwidth_required": "high",
            "created_at": datetime.now().isoformat(),
        }
        
        return {
            "agent": self.name,
            "call_request": call_request,
            "estimated_wait": random.randint(5, 30),
            "recommendations": [
                "Prepare photos or messages to share",
                "Test camera and microphone",
                "Have questions ready for family",
            ],
            "timestamp": datetime.now().isoformat(),
        }
