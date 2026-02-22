import random
import uuid
from datetime import datetime
from typing import Dict, Any, List
from .base_agent import BaseAgent


class ExerciseAgent(BaseAgent):
    """Generates personalized microgravity workouts with form correction"""

    def __init__(self, agent_id: str = None):
        super().__init__(
            agent_id=agent_id or "exercise_agent",
            name="Exercise Coach",
            agent_type="physical",
            capabilities=[
                "workout_generation",
                "form_correction",
                "progress_tracking",
                "microgravity_adaptation",
            ],
        )
        
        self.exercise_types = {
            " resistance": [
                {"name": "ARED (Advanced Resistive Exercise Device)", "duration": 15, "sets": 6},
                {"name": "Squat", "duration": 10, "sets": 3},
                {"name": "Deadlift", "duration": 10, "sets": 3},
                {"name": "Heel Raise", "duration": 8, "sets": 3},
            ],
            "cardio": [
                {"name": "CEVIS (Cycle Ergometer with Vibration Isolation)", "duration": 30, "sets": 1},
                {"name": "T2 Treadmill", "duration": 30, "sets": 1},
                {"name": "COLUMBIA (Upper Body Ergometer)", "duration": 20, "sets": 1},
            ],
            "flexibility": [
                {"name": "Yoga Stretch", "duration": 15, "sets": 1},
                {"name": "Foam Rolling", "duration": 10, "sets": 1},
                {"name": "Dynamic Warm-up", "duration": 8, "sets": 1},
            ],
        }
        
        self.workout_history = []
        self.last_workout = None

    async def process(self, input_data: Dict[str, Any]) -> Dict[str, Any]:
        """Process exercise request"""
        action = input_data.get("action", "generate_workout")
        
        if action == "generate_workout":
            return await self._generate_workout(input_data)
        elif action == "get_daily_plan":
            return await self._get_daily_plan()
        elif action == "log_workout":
            return await self._log_workout(input_data)
        elif action == "get_progress":
            return await self._get_progress()
        else:
            return {"error": f"Unknown action: {action}"}

    async def _generate_workout(self, data: Dict) -> Dict[str, Any]:
        """Generate personalized workout based on astronaut state"""
        focus_area = data.get("focus", random.choice(["resistance", "cardio", "flexibility"]))
        intensity = data.get("intensity", "moderate")
        available_time = data.get("time_available", 45)
        
        exercises = []
        total_time = 0
        
        category_exercises = self.exercise_types.get(focus_area, self.exercise_types["resistance"])
        
        for exercise in random.sample(category_exercises, min(3, len(category_exercises))):
            if total_time + exercise["duration"] <= available_time - 5:
                exercises.append({
                    **exercise,
                    "intensity": intensity,
                    "form_cues": self._get_form_cues(exercise["name"]),
                })
                total_time += exercise["duration"]
        
        warmup = [
            {"name": "Jumping Jacks (Zero-G)", "duration": 3, "sets": 1},
            {"name": "Arm Circles", "duration": 2, "sets": 1},
        ]
        
        cooldown = [
            {"name": "Static Stretching", "duration": 5, "sets": 1},
        ]
        
        workout = {
            "id": str(uuid.uuid4()),
            "type": focus_area,
            "intensity": intensity,
            "estimated_duration": total_time + 10,
            "warmup": warmup,
            "main_exercises": exercises,
            "cooldown": cooldown,
            "calories_burned_estimate": self._estimate_calories(exercises),
            "bone_density_impact": "high" if focus_area == "resistance" else "moderate",
            "created_at": datetime.now().isoformat(),
        }
        
        self.update_status("idle")
        return {
            "agent": self.name,
            "workout": workout,
            "timestamp": datetime.now().isoformat(),
        }

    def _get_form_cues(self, exercise_name: str) -> List[str]:
        """Get form correction cues for exercises"""
        cues = {
            "ARED": [
                "Maintain neutral spine",
                "Engage core throughout movement",
                "Breathe steadily during resistance",
            ],
            "CEVIS": [
                "Maintain consistent cadence",
                "Keep back straight",
                "Adjust resistance gradually",
            ],
            "default": [
                "Focus on controlled movements",
                "Maintain proper breathing",
            ],
        }
        return cues.get(exercise_name, cues["default"])

    def _estimate_calories(self, exercises: List[Dict]) -> int:
        """Estimate calories burned"""
        base_calories = sum(ex.get("duration", 10) * ex.get("sets", 1) for ex in exercises)
        return int(base_calories * 5)

    async def _get_daily_plan(self) -> Dict[str, Any]:
        """Get recommended daily exercise plan"""
        return {
            "agent": self.name,
            "daily_plan": {
                "morning": {
                    "type": "cardio",
                    "duration": 30,
                    "purpose": "Wake up body, boost energy",
                },
                "afternoon": {
                    "type": "resistance",
                    "duration": 45,
                    "purpose": "Bone density maintenance",
                },
                "evening": {
                    "type": "flexibility",
                    "duration": 15,
                    "purpose": "Recovery and relaxation",
                },
            },
            "total_daily_duration": 90,
            "timestamp": datetime.now().isoformat(),
        }

    async def _log_workout(self, data: Dict) -> Dict[str, Any]:
        """Log completed workout"""
        workout_log = {
            "id": str(uuid.uuid4()),
            "workout_id": data.get("workout_id"),
            "completed_at": datetime.now().isoformat(),
            "actual_duration": data.get("duration", 0),
            "exercises_completed": data.get("exercises", []),
            "feedback": data.get("feedback", ""),
        }
        
        self.workout_history.append(workout_log)
        self.last_workout = workout_log
        
        return {
            "agent": self.name,
            "logged": workout_log,
            "streak_days": len(set(w["completed_at"][:10] for w in self.workout_history)),
            "timestamp": datetime.now().isoformat(),
        }

    async def _get_progress(self) -> Dict[str, Any]:
        """Get workout progress statistics"""
        if not self.workout_history:
            return {
                "agent": self.name,
                "progress": {
                    "total_workouts": 0,
                    "this_week": 0,
                    "average_duration": 0,
                },
                "timestamp": datetime.now().isoformat(),
            }
        
        this_week = [
            w for w in self.workout_history
            if datetime.fromisoformat(w["completed_at"]).isocalendar()[1] 
            == datetime.now().isocalendar()[1]
        ]
        
        return {
            "agent": self.name,
            "progress": {
                "total_workouts": len(self.workout_history),
                "this_week": len(this_week),
                "average_duration": sum(w["actual_duration"] for w in self.workout_history) / len(self.workout_history),
                "last_workout": self.last_workout,
            },
            "timestamp": datetime.now().isoformat(),
        }
