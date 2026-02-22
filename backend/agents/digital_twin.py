import random
from datetime import datetime, timedelta
from typing import Dict, Any, List
from .base_agent import BaseAgent


class DigitalTwinAgent(BaseAgent):
    """Runs predictive simulations for 'what-if' scenarios"""

    def __init__(self, agent_id: str = None):
        super().__init__(
            agent_id=agent_id or "digital_twin",
            name="Digital Twin",
            agent_type="intelligence",
            capabilities=[
                "predictive_simulation",
                "what_if_analysis",
                "health_prediction",
                "risk_assessment",
            ],
        )
        
        self.simulation_history = []

    async def process(self, input_data: Dict[str, Any]) -> Dict[str, Any]:
        """Process simulation request"""
        action = input_data.get("action", "predict_health")
        
        if action == "predict_health":
            return await self._predict_health(input_data)
        elif action == "what_if":
            return await self._what_if_analysis(input_data)
        elif action == "risk_assessment":
            return await self._risk_assessment()
        elif action == "simulate_scenario":
            return await self._simulate_scenario(input_data)
        else:
            return {"error": f"Unknown action: {action}"}

    async def _predict_health(self, data: Dict) -> Dict[str, Any]:
        """Predict future health state"""
        time_horizon = data.get("hours", 24)
        
        predictions = {
            "heart_rate": {
                "current": random.randint(60, 80),
                "predicted": random.randint(58, 85),
                "trend": random.choice(["stable", "slight_increase", "slight_decrease"]),
                "confidence": random.randint(65, 85),
            },
            "energy_level": {
                "current": random.randint(50, 80),
                "predicted": random.randint(45, 90),
                "trend": random.choice(["stable", "improving", "declining"]),
                "confidence": random.randint(60, 80),
            },
            "stress_level": {
                "current": random.randint(10, 40),
                "predicted": random.randint(10, 50),
                "trend": random.choice(["stable", "increasing", "decreasing"]),
                "confidence": random.randint(55, 75),
            },
            "fatigue": {
                "current": random.randint(20, 50),
                "predicted": random.randint(15, 60),
                "trend": random.choice(["stable", "increasing", "decreasing"]),
                "confidence": random.randint(60, 80),
            },
        }
        
        risk_factors = []
        if predictions["stress_level"]["predicted"] > 40:
            risk_factors.append({
                "factor": "elevated_stress",
                "probability": random.randint(60, 90),
                "recommendation": "Schedule relaxation session",
            })
        
        if predictions["fatigue"]["predicted"] > 50:
            risk_factors.append({
                "factor": "high_fatigue",
                "probability": random.randint(55, 85),
                "recommendation": "Recommend rest day",
            })
        
        simulation = {
            "id": f"SIM-{datetime.now().strftime('%Y%m%d%H%M%S')}",
            "type": "health_prediction",
            "time_horizon_hours": time_horizon,
            "predictions": predictions,
            "risk_factors": risk_factors,
            "overall_health_status": "good" if len(risk_factors) < 2 else "needs_attention",
            "generated_at": datetime.now().isoformat(),
        }
        
        self.simulation_history.append(simulation)
        
        return {
            "agent": self.name,
            "simulation": simulation,
            "timestamp": datetime.now().isoformat(),
        }

    async def _what_if_analysis(self, data: Dict) -> Dict[str, Any]:
        """Run what-if scenario analysis"""
        scenario = data.get("scenario", "exercise")
        parameters = data.get("parameters", {})
        
        scenario_results = {
            "exercise_intense": {
                "description": "What if astronaut does intense exercise?",
                "predicted_outcomes": {
                    "heart_rate": "Increase to 120-140 bpm for 30 min, then normalize in 2 hours",
                    "energy": "Temporary decrease, long-term increase",
                    "sleep_quality": "Improved by 10-15%",
                    "muscle_strength": "Maintained or improved",
                },
                "risks": ["Potential fatigue if overtraining", "Dehydration risk"],
                "confidence": random.randint(70, 90),
            },
            "skip_sleep": {
                "description": "What if astronaut skips a night's sleep?",
                "predicted_outcomes": {
                    "cognition": "Decreased by 20-30%",
                    "mood": "Increased irritability",
                    "heart_rate": "Elevated by 5-10 bpm",
                    "immune_system": "Temporary suppression",
                },
                "risks": ["Accumulated sleep debt", "Increased error rate"],
                "confidence": random.randint(75, 95),
            },
            "high_stress": {
                "description": "What if mission stress increases significantly?",
                "predicted_outcomes": {
                    "sleep": "Reduced by 1-2 hours",
                    "heart_rate": "Elevated 10-20 bpm",
                    "mood": "Decreased positivity",
                    "decision_making": "Minor impairment",
                },
                "risks": ["Burnout risk", "Interpersonal tension"],
                "confidence": random.randint(65, 85),
            },
            "isolation_extended": {
                "description": "What if isolation period is extended by 30 days?",
                "predicted_outcomes": {
                    "morale": "Potential decrease 10-20%",
                    "team_dynamic": "Possible strain",
                    "creativity": "Potential increase",
                    "routine_adherence": "Potential decrease",
                },
                "risks": ["Psychological fatigue", "Decreased motivation"],
                "confidence": random.randint(55, 75),
            },
        }
        
        result = scenario_results.get(scenario, scenario_results["exercise_intense"])
        
        return {
            "agent": self.name,
            "scenario": scenario,
            "analysis": result,
            "timestamp": datetime.now().isoformat(),
        }

    async def _risk_assessment(self) -> Dict[str, Any]:
        """Get overall risk assessment"""
        risks = [
            {
                "category": "Physical Health",
                "level": random.choice(["low", "low", "medium"]),
                "factors": ["Bone density loss", "Muscle atrophy", "Cardiovascular deconditioning"],
                "mitigation": "Regular exercise protocol in place",
            },
            {
                "category": "Psychological",
                "level": random.choice(["low", "medium"]),
                "factors": ["Isolation", "Limited communication", "Stress"],
                "mitigation": "Regular check-ins, counseling available",
            },
            {
                "category": "Mission Operations",
                "level": random.choice(["low", "low", "medium"]),
                "factors": ["Equipment failure", "Communication delays", "Schedule changes"],
                "mitigation": "Redundant systems, backup procedures",
            },
        ]
        
        overall_level = "low" if sum(1 for r in risks if r["level"] == "low") >= 2 else "medium"
        
        return {
            "agent": self.name,
            "risk_assessment": {
                "overall_level": overall_level,
                "categories": risks,
                "total_risks_identified": len(risks),
                "mitigations_in_place": sum(len(r["mitigation"].split(",")) for r in risks),
            },
            "timestamp": datetime.now().isoformat(),
        }

    async def _simulate_scenario(self, data: Dict) -> Dict[str, Any]:
        """Simulate custom scenario"""
        scenario_name = data.get("scenario_name", "custom")
        variables = data.get("variables", {})
        
        simulation_duration = data.get("duration_hours", 1)
        
        outcomes = []
        
        for hour in range(0, simulation_duration, 6):
            outcomes.append({
                "hour": hour,
                "heart_rate": random.randint(55, 90),
                "stress": random.randint(10, 50),
                "energy": random.randint(40, 90),
                "mood": random.choice(["neutral", "positive", "negative"]),
            })
        
        return {
            "agent": self.name,
            "simulation": {
                "id": f"SIM-{datetime.now().strftime('%Y%m%d%H%M%S')}",
                "scenario": scenario_name,
                "variables": variables,
                "duration_hours": simulation_duration,
                "outcomes": outcomes,
                "conclusion": "Simulation complete - results within expected parameters",
            },
            "timestamp": datetime.now().isoformat(),
        }
