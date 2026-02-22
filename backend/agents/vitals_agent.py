import uuid
import random
from datetime import datetime, timedelta
from typing import Dict, Any, List
from .base_agent import BaseAgent, AgentState


class VitalsAgent(BaseAgent):
    """Monitors astronaut health vitals - heart rate, O2, CO2, temperature"""

    def __init__(self, agent_id: str = None):
        super().__init__(
            agent_id=agent_id or "vitals_agent",
            name="Vitals Monitor",
            agent_type="physical",
            capabilities=[
                "heart_rate_monitoring",
                "o2_saturation",
                "co2_monitoring",
                "temperature_tracking",
                "anomaly_detection",
            ],
        )
        self.vitals_history = []
        self.baseline = {
            "heart_rate": 68,
            "o2_saturation": 98,
            "co2_level": 0.4,
            "temperature": 36.8,
        }

    async def process(self, input_data: Dict[str, Any]) -> Dict[str, Any]:
        """Process vitals monitoring request"""
        action = input_data.get("action", "get_current")

        if action == "get_current":
            return await self._get_current_vitals()
        elif action == "check_anomalies":
            return await self._detect_anomalies(input_data.get("history", []))
        elif action == "update_baseline":
            return await self._update_baseline(input_data)
        else:
            return {"error": f"Unknown action: {action}"}

    async def _get_current_vitals(self) -> Dict[str, Any]:
        """Generate realistic vitals based on circadian rhythm and activity"""
        now = datetime.now()
        hour = now.hour
        
        circadian_factor = 1 + 0.15 * self._sin(2 * 3.14159 * (hour - 6) / 24)
        
        activity_factor = random.uniform(1.0, 1.3) if random.random() > 0.7 else 1.0
        stress_factor = random.uniform(1.0, 1.2)
        
        heart_rate = (
            self.baseline["heart_rate"] 
            * circadian_factor 
            * activity_factor 
            * stress_factor
            + random.gauss(0, 3)
        )
        
        o2_saturation = (
            self.baseline["o2_saturation"]
            - (activity_factor - 1) * 2
            + random.gauss(0, 0.3)
        )
        
        co2_level = self.baseline["co2_level"] + (activity_factor - 1) * 0.1
        temperature = self.baseline["temperature"] + (stress_factor - 1) * 0.3
        
        vitals = {
            "heart_rate": round(heart_rate, 1),
            "o2_saturation": round(max(92, min(100, o2_saturation)), 1),
            "co2_level": round(co2_level, 2),
            "temperature": round(temperature, 1),
            "hr_variability": round(random.uniform(30, 80), 1),
            "timestamp": now.isoformat(),
        }
        
        self.vitals_history.append(vitals)
        if len(self.vitals_history) > 1000:
            self.vitals_history.pop(0)
            
        self.update_status("idle")
        
        return {
            "agent": self.name,
            "vitals": vitals,
            "status": "normal" if self._is_normal(vitals) else "warning",
            "timestamp": now.isoformat(),
        }

    def _sin(self, x):
        """Simple sin approximation"""
        return x - x**3/6 + x**5/120

    def _is_normal(self, vitals: Dict) -> bool:
        """Check if vitals are within normal range"""
        thresholds = {
            "heart_rate": (50, 120),
            "o2_saturation": (92, 100),
            "co2_level": (0, 0.8),
            "temperature": (35.5, 38.5),
        }
        
        for metric, (min_val, max_val) in thresholds.items():
            value = vitals.get(metric)
            if value is not None and (value < min_val or value > max_val):
                return False
        return True

    async def _detect_anomalies(self, history: List[Dict]) -> Dict[str, Any]:
        """Detect anomalies in vitals"""
        if not history:
            history = self.vitals_history[-10:]
            
        anomalies = []
        thresholds = {
            "heart_rate": {"min": 50, "max": 120},
            "o2_saturation": {"min": 92, "max": 100},
            "co2_level": {"min": 0, "max": 0.8},
            "temperature": {"min": 35.5, "max": 38.5},
        }
        
        current = history[-1] if history else {}
        
        for metric, (min_val, max_val) in thresholds.items():
            value = current.get(metric)
            if value is not None:
                if value < min_val:
                    severity = "critical" if value < min_val * 0.9 else "warning"
                    anomalies.append({
                        "metric": metric,
                        "value": value,
                        "threshold": "low",
                        "severity": severity,
                    })
                elif value > max_val:
                    severity = "critical" if value > max_val * 1.1 else "warning"
                    anomalies.append({
                        "metric": metric,
                        "value": value,
                        "threshold": "high",
                        "severity": severity,
                    })
        
        if len(history) >= 3:
            recent = history[-3:]
            for metric in ["heart_rate", "o2_saturation"]:
                values = [v.get(metric) for v in recent if v.get(metric)]
                if len(values) == 3:
                    if values[0] < values[1] < values[2] and metric == "heart_rate" and values[2] > 100:
                        anomalies.append({
                            "metric": metric,
                            "trend": "increasing",
                            "severity": "warning",
                        })
        
        return {
            "agent": self.name,
            "anomalies": anomalies,
            "has_critical": any(a.get("severity") == "critical" for a in anomalies),
            "timestamp": datetime.now().isoformat(),
        }

    async def _update_baseline(self, data: Dict) -> Dict:
        """Update baseline vitals"""
        if "heart_rate" in data:
            self.baseline["heart_rate"] = data["heart_rate"]
        if "o2_saturation" in data:
            self.baseline["o2_saturation"] = data["o2_saturation"]
        if "temperature" in data:
            self.baseline["temperature"] = data["temperature"]
            
        return {
            "agent": self.name,
            "baseline": self.baseline,
            "timestamp": datetime.now().isoformat(),
        }
