import random
from datetime import datetime, timedelta
from typing import Dict, Any, List
from .base_agent import BaseAgent


class SleepAgent(BaseAgent):
    """Analyzes sleep cycles and provides optimization recommendations"""

    def __init__(self, agent_id: str = None):
        super().__init__(
            agent_id=agent_id or "sleep_agent",
            name="Sleep Analyst",
            agent_type="physical",
            capabilities=[
                "sleep_cycle_analysis",
                "circadian_optimization",
                "sleep_quality_scoring",
                "recommendation_generation",
            ],
        )
        
        self.sleep_history = []
        self.sleep_stages = ["Awake", "Light", "Deep", "REM"]

    async def process(self, input_data: Dict[str, Any]) -> Dict[str, Any]:
        """Process sleep analysis request"""
        action = input_data.get("action", "analyze_sleep")
        
        if action == "analyze_sleep":
            return await self._analyze_sleep(input_data)
        elif action == "get_recommendations":
            return await self._get_recommendations()
        elif action == "get_quality_score":
            return await self._get_quality_score()
        elif action == "optimize_schedule":
            return await self._optimize_schedule(input_data)
        else:
            return {"error": f"Unknown action: {action}"}

    async def _analyze_sleep(self, data: Dict) -> Dict[str, Any]:
        """Analyze sleep patterns"""
        date = data.get("date", datetime.now().date())
        
        stages = self._generate_sleep_stages()
        
        analysis = {
            "date": date.isoformat(),
            "total_duration": random.randint(300, 480),
            "stages": stages,
            "sleep_cycles": len([s for s in stages if s["stage"] == "Deep"]),
            "wake_ups": random.randint(0, 3),
            "time_to_sleep": random.randint(5, 30),
            "sleep_efficiency": round(random.uniform(85, 95), 1),
        }
        
        sleep_record = {
            "date": date.isoformat(),
            "analysis": analysis,
            "quality_score": self._calculate_quality_score(analysis),
        }
        
        self.sleep_history.append(sleep_record)
        
        return {
            "agent": self.name,
            "analysis": analysis,
            "quality_score": sleep_record["quality_score"],
            "recommendations": self._generate_recommendations(analysis),
            "timestamp": datetime.now().isoformat(),
        }

    def _generate_sleep_stages(self) -> List[Dict]:
        """Generate simulated sleep stage data"""
        stages = []
        duration = random.randint(300, 480)
        cycle_length = 90
        
        for minute in range(0, duration, cycle_length):
            stages.append({
                "minute": minute,
                "stage": "REM",
                "duration": random.randint(15, 30),
            })
            stages.append({
                "minute": minute + 25,
                "stage": "Light",
                "duration": random.randint(20, 35),
            })
            stages.append({
                "minute": minute + 55,
                "stage": "Deep",
                "duration": random.randint(15, 25),
            })
        
        return stages[:20]

    def _calculate_quality_score(self, analysis: Dict) -> Dict[str, Any]:
        """Calculate overall sleep quality score"""
        score = 70
        
        efficiency = analysis.get("sleep_efficiency", 90)
        score += (efficiency - 85) * 2
        
        wake_ups = analysis.get("wake_ups", 0)
        score -= wake_ups * 3
        
        total_duration = analysis.get("total_duration", 360)
        if 420 <= total_duration <= 540:
            score += 10
        elif total_duration < 360:
            score -= 10
        
        cycles = analysis.get("sleep_cycles", 4)
        score += min(cycles, 5) * 2
        
        score = max(0, min(100, score))
        
        quality = "Excellent" if score >= 85 else "Good" if score >= 70 else "Fair" if score >= 50 else "Poor"
        
        return {
            "score": round(score, 1),
            "quality": quality,
            "factors": {
                "efficiency": efficiency,
                "duration": total_duration,
                "cycles": cycles,
            },
        }

    def _generate_recommendations(self, analysis: Dict) -> List[str]:
        """Generate sleep improvement recommendations"""
        recommendations = []
        
        if analysis.get("wake_ups", 0) > 2:
            recommendations.append("Consider adjusting room temperature (cooler is better)")
            recommendations.append("Limit fluid intake before bed")
        
        if analysis.get("time_to_sleep", 15) > 20:
            recommendations.append("Try relaxation techniques before bed")
            recommendations.append("Avoid screens 1 hour before sleep")
        
        if analysis.get("total_duration", 400) < 360:
            recommendations.append("Try to get at least 7-8 hours of sleep")
            recommendations.append("Consider a 20-minute power nap during the day")
        
        deep_cycles = analysis.get("sleep_cycles", 0)
        if deep_cycles < 3:
            recommendations.append("Avoid alcohol before bed (reduces deep sleep)")
        
        if not recommendations:
            recommendations.append("Sleep quality is excellent! Maintain current routine")
        
        return recommendations

    async def _get_recommendations(self) -> Dict[str, Any]:
        """Get general sleep recommendations"""
        return {
            "agent": self.name,
            "recommendations": [
                "Maintain consistent sleep/wake schedule even on weekends",
                "Keep sleep environment cool (18-21°C)",
                "Use blackout curtains to block light",
                "Consider white noise for sound isolation",
                "Avoid caffeine 6 hours before bedtime",
                "Exercise regularly but not within 3 hours of sleep",
                "Use sleep mask and earplugs if needed",
            ],
            "circadian_tips": [
                "Get bright light exposure in the morning",
                "Dim lights 2 hours before bedtime",
                "Avoid blue light from screens",
                "Use red/orange light for nighttime navigation",
            ],
            "timestamp": datetime.now().isoformat(),
        }

    async def _get_quality_score(self) -> Dict[str, Any]:
        """Get overall sleep quality based on history"""
        if not self.sleep_history:
            return {
                "agent": self.name,
                "current_score": None,
                "weekly_average": None,
                "trend": "no_data",
                "timestamp": datetime.now().isoformat(),
            }
        
        recent = self.sleep_history[-7:]
        scores = [s["quality_score"]["score"] for s in recent]
        avg = sum(scores) / len(scores)
        
        trend = "improving" if len(scores) >= 3 and scores[-1] > scores[-3] else "stable"
        
        return {
            "agent": self.name,
            "current_score": scores[-1] if scores else None,
            "weekly_average": round(avg, 1),
            "trend": trend,
            "history": [{"date": s["date"], "score": s["quality_score"]["score"]} for s in recent],
            "timestamp": datetime.now().isoformat(),
        }

    async def _optimize_schedule(self, data: Dict) -> Dict[str, Any]:
        """Optimize sleep schedule based on mission timeline"""
        wake_time = data.get("wake_time", "06:00")
        bedtime = data.get("bedtime", "22:30")
        
        optimal_bedtime = "22:00"
        optimal_wake = "06:00"
        
        adjustment_needed = bedtime != optimal_bedtime
        
        return {
            "agent": self.name,
            "current_schedule": {
                "bedtime": bedtime,
                "wake_time": wake_time,
            },
            "recommended_schedule": {
                "bedtime": optimal_bedtime,
                "wake_time": optimal_wake,
            },
            "adjustment": adjustment_needed,
            "reason": "Aligns with circadian rhythm for optimal rest" if adjustment_needed else "Schedule is optimal",
            "timestamp": datetime.now().isoformat(),
        }
