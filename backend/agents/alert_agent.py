import random
from datetime import datetime
from typing import Dict, Any, List
from .base_agent import BaseAgent


class AlertAgent(BaseAgent):
    """Detects emergencies and initiates protocols"""

    def __init__(self, agent_id: str = None):
        super().__init__(
            agent_id=agent_id or "alert_agent",
            name="Alert System",
            agent_type="intelligence",
            capabilities=[
                "emergency_detection",
                "severity_classification",
                "protocol_initiation",
                "crew_notification",
            ],
        )
        
        self.alert_history = []
        self.active_alerts = []
        
        self.severity_levels = {
            1: {"name": "EMERGENCY", "color": "red", "action": "Immediate response required"},
            2: {"name": "CRITICAL", "color": "orange", "action": "Response within minutes"},
            3: {"name": "WARNING", "color": "yellow", "action": "Response within hour"},
            4: {"name": "INFO", "color": "blue", "action": "Awareness only"},
        }

    async def process(self, input_data: Dict[str, Any]) -> Dict[str, Any]:
        """Process alert request"""
        action = input_data.get("action", "get_status")
        
        if action == "get_status":
            return await self._get_status()
        elif action == "create_alert":
            return await self._create_alert(input_data)
        elif action == "get_alerts":
            return await self._get_alerts(input_data)
        elif action == "acknowledge_alert":
            return await self._acknowledge_alert(input_data)
        elif action == "resolve_alert":
            return await self._resolve_alert(input_data)
        elif action == "get_protocol":
            return await self._get_protocol(input_data)
        else:
            return {"error": f"Unknown action: {action}"}

    async def _get_status(self) -> Dict[str, Any]:
        """Get current alert status"""
        critical_count = len([a for a in self.active_alerts if a.get("severity") <= 2])
        
        return {
            "agent": self.name,
            "active_alerts": len(self.active_alerts),
            "critical_count": critical_count,
            "last_alert": self.alert_history[-1] if self.alert_history else None,
            "system_status": "NORMAL" if critical_count == 0 else "ALERT",
            "timestamp": datetime.now().isoformat(),
        }

    async def _create_alert(self, data: Dict) -> Dict[str, Any]:
        """Create new alert"""
        alert_type = data.get("type", "unknown")
        severity = data.get("severity", 4)
        message = data.get("message", "")
        source = data.get("source", "system")
        
        severity_info = self.severity_levels.get(severity, self.severity_levels[4])
        
        alert = {
            "id": f"ALT-{datetime.now().strftime('%Y%m%d-%H%M%S')}-{random.randint(100, 999)}",
            "type": alert_type,
            "severity": severity,
            "severity_name": severity_info["name"],
            "message": message,
            "source": source,
            "created_at": datetime.now().isoformat(),
            "acknowledged": False,
            "resolved": False,
        }
        
        self.active_alerts.append(alert)
        self.alert_history.append(alert)
        
        if severity <= 2:
            self.update_status("alert")
        
        return {
            "agent": self.name,
            "alert": alert,
            "action_required": severity_info["action"],
            "protocol": self._get_protocol_for_type(alert_type),
            "timestamp": datetime.now().isoformat(),
        }

    async def _get_alerts(self, data: Dict) -> Dict[str, Any]:
        """Get alerts with optional filtering"""
        alert_type = data.get("type")
        severity = data.get("severity")
        status = data.get("status", "active")
        
        alerts = self.active_alerts if status == "active" else self.alert_history
        
        if alert_type:
            alerts = [a for a in alerts if a.get("type") == alert_type]
        if severity:
            alerts = [a for a in alerts if a.get("severity") == severity]
        
        return {
            "agent": self.name,
            "alerts": alerts,
            "count": len(alerts),
            "timestamp": datetime.now().isoformat(),
        }

    async def _acknowledge_alert(self, data: Dict) -> Dict[str, Any]:
        """Acknowledge an alert"""
        alert_id = data.get("alert_id")
        
        for alert in self.active_alerts:
            if alert.get("id") == alert_id:
                alert["acknowledged"] = True
                alert["acknowledged_at"] = datetime.now().isoformat()
                break
        
        return {
            "agent": self.name,
            "alert_id": alert_id,
            "status": "acknowledged",
            "timestamp": datetime.now().isoformat(),
        }

    async def _resolve_alert(self, data: Dict) -> Dict[str, Any]:
        """Resolve an alert"""
        alert_id = data.get("alert_id")
        resolution = data.get("resolution", "")
        
        for alert in self.active_alerts:
            if alert.get("id") == alert_id:
                alert["resolved"] = True
                alert["resolved_at"] = datetime.now().isoformat()
                alert["resolution"] = resolution
                self.active_alerts.remove(alert)
                break
        
        return {
            "agent": self.name,
            "alert_id": alert_id,
            "status": "resolved",
            "timestamp": datetime.now().isoformat(),
        }

    async def _get_protocol(self, data: Dict) -> Dict[str, Any]:
        """Get emergency protocol"""
        alert_type = data.get("type", "general")
        
        protocol = self._get_protocol_for_type(alert_type)
        
        return {
            "agent": self.name,
            "protocol": protocol,
            "timestamp": datetime.now().isoformat(),
        }

    def _get_protocol_for_type(self, alert_type: str) -> Dict[str, Any]:
        """Get protocol for alert type"""
        protocols = {
            "vitals": {
                "name": "Medical Emergency Protocol",
                "steps": [
                    "Assess astronaut condition",
                    "Check vital signs",
                    "Contact mission control",
                    "Prepare medical supplies",
                    "Document all actions",
                ],
                "contacts": ["Mission Control", "Flight Surgeon", "Emergency Services"],
            },
            "psychological": {
                "name": "Psychological Crisis Protocol",
                "steps": [
                    "Ensure astronaut safety",
                    "Provide immediate support",
                    "Alert mission psychologist",
                    "Notify family if needed",
                    "Monitor continuously",
                ],
                "contacts": ["Mission Psychologist", "Mission Control"],
            },
            "system": {
                "name": "System Failure Protocol",
                "steps": [
                    "Identify failed system",
                    "Assess impact on mission",
                    "Implement backup procedures",
                    "Notify mission control",
                    "Document incident",
                ],
                "contacts": ["Mission Control", "Engineering Team"],
            },
            "environmental": {
                "name": "Environmental Hazard Protocol",
                "steps": [
                    "Assess hazard type",
                    "Activate appropriate containment",
                    "Evacuate if necessary",
                    "Notify mission control",
                    "Monitor continuously",
                ],
                "contacts": ["Mission Control", "Environmental Control"],
            },
            "default": {
                "name": "General Emergency Protocol",
                "steps": [
                    "Assess situation",
                    "Ensure crew safety",
                    "Notify mission control",
                    "Document incident",
                    "Follow standard procedures",
                ],
                "contacts": ["Mission Control"],
            },
        }
        
        return protocols.get(alert_type, protocols["default"])
