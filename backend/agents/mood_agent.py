import random
from datetime import datetime
from typing import Dict, Any, List
from .base_agent import BaseAgent


class MoodAgent(BaseAgent):
    """Analyzes text/speech for emotional state detection"""

    def __init__(self, agent_id: str = None):
        super().__init__(
            agent_id=agent_id or "mood_agent",
            name="Mood Detector",
            agent_type="psychological",
            capabilities=[
                "sentiment_analysis",
                "emotion_detection",
                "mood_tracking",
                "stress_indicator",
            ],
        )
        
        self.positive_words = [
            "good", "great", "happy", "excellent", "love", "wonderful", 
            "amazing", "fantastic", "joy", "excited", "grateful", "blessed",
        ]
        
        self.negative_words = [
            "bad", "terrible", "awful", "hate", "miserable", "horrible", 
            "angry", "frustrated", "annoyed", "furious", "disgusted",
        ]
        
        self.anxiety_words = [
            "nervous", "scared", "worried", "anxious", "panic", "fear",
            "tense", "uneasy", "apprehensive", "freaked",
        ]
        
        self.mood_history = []

    async def process(self, input_data: Dict[str, Any]) -> Dict[str, Any]:
        """Process mood analysis request"""
        action = input_data.get("action", "analyze_mood")
        
        if action == "analyze_mood":
            return await self._analyze_mood(input_data)
        elif action == "get_mood_trend":
            return await self._get_mood_trend()
        elif action == "correlate_vitals":
            return await self._correlate_with_vitals(input_data)
        else:
            return {"error": f"Unknown action: {action}"}

    async def _analyze_mood(self, data: Dict) -> Dict[str, Any]:
        """Analyze emotion from text and vitals"""
        text = data.get("text", "")
        vitals = data.get("vitals", {})
        
        text_lower = text.lower()
        
        sentiment_score = 0
        
        for word in self.positive_words:
            if word in text_lower:
                sentiment_score += 1
        
        for word in self.negative_words:
            if word in text_lower:
                sentiment_score -= 1.5
        
        for word in self.anxiety_words:
            if word in text_lower:
                sentiment_score -= 2
        
        physiological_factor = 0
        if vitals:
            hr = vitals.get("heart_rate", 70)
            if hr > 90:
                physiological_factor -= 1
            elif hr < 60:
                physiological_factor -= 0.5
            
            hr_variability = vitals.get("hr_variability", 50)
            if hr_variability < 30:
                physiological_factor -= 1
        
        total_score = sentiment_score + physiological_factor
        
        emotion = self._determine_emotion(total_score, text_lower)
        
        confidence = min(100, max(0, (abs(total_score) + 5) * 10))
        
        analysis = {
            "emotion": emotion,
            "score": round(total_score, 1),
            "confidence": round(confidence, 1),
            "text_sentiment": "positive" if total_score > 0.5 else "negative" if total_score < -0.5 else "neutral",
            "physiological_state": "stressed" if vitals and vitals.get("heart_rate", 70) > 90 else "calm",
            "contributing_factors": {
                "text_analysis": self._get_contributing_factors(text_lower),
                "physiological": "elevated heart rate" if physiological_factor < 0 and vitals else "normal",
            },
        }
        
        mood_record = {
            "timestamp": datetime.now().isoformat(),
            "text_preview": text[:50] + "..." if len(text) > 50 else text,
            "analysis": analysis,
        }
        
        self.mood_history.append(mood_record)
        
        return {
            "agent": self.name,
            "mood_analysis": analysis,
            "timestamp": datetime.now().isoformat(),
        }

    def _determine_emotion(self, score: float, text: str) -> str:
        """Determine emotion from score"""
        if any(word in text for word in self.anxiety_words):
            return "anxious"
        
        if score >= 3:
            return "very_happy"
        elif score >= 1:
            return "happy"
        elif score >= -1:
            return "neutral"
        elif score >= -3:
            return "sad"
        else:
            return "distressed"

    def _get_contributing_factors(self, text: str) -> str:
        """Get factors contributing to mood"""
        factors = []
        
        for word in self.positive_words:
            if word in text:
                factors.append(f"positive: {word}")
        
        for word in self.negative_words + self.anxiety_words:
            if word in text:
                factors.append(f"negative: {word}")
        
        return factors if factors else ["neutral language"]

    async def _get_mood_trend(self) -> Dict[str, Any]:
        """Get mood trend over time"""
        if not self.mood_history:
            return {
                "agent": self.name,
                "trend": "no_data",
                "timestamp": datetime.now().isoformat(),
            }
        
        recent = self.mood_history[-24:]
        scores = [m["analysis"]["score"] for m in recent]
        
        if len(scores) >= 3:
            if scores[-1] > scores[-3]:
                trend = "improving"
            elif scores[-1] < scores[-3]:
                trend = "declining"
            else:
                trend = "stable"
        else:
            trend = "insufficient_data"
        
        avg_score = sum(scores) / len(scores) if scores else 0
        
        emotions_count = {}
        for m in recent:
            emotion = m["analysis"]["emotion"]
            emotions_count[emotion] = emotions_count.get(emotion, 0) + 1
        
        return {
            "agent": self.name,
            "trend": trend,
            "average_score": round(avg_score, 1),
            "sample_size": len(scores),
            "emotion_distribution": emotions_count,
            "dominant_emotion": max(emotions_count, key=emotions_count.get) if emotions_count else "unknown",
            "timestamp": datetime.now().isoformat(),
        }

    async def _correlate_with_vitals(self, data: Dict) -> Dict[str, Any]:
        """Correlate mood with physiological data"""
        vitals = data.get("vitals", {})
        
        if not vitals:
            return {
                "agent": self.name,
                "correlation": "no_vitals_data",
                "timestamp": datetime.now().isoformat(),
            }
        
        hr = vitals.get("heart_rate", 70)
        o2 = vitals.get("o2_saturation", 98)
        
        correlation = []
        
        if hr > 90:
            correlation.append({
                "metric": "heart_rate",
                "status": "elevated",
                "mood_impact": "suggests stress or anxiety",
                "recommendation": "Consider relaxation techniques",
            })
        
        if o2 < 95:
            correlation.append({
                "metric": "o2_saturation",
                "status": "low",
                "mood_impact": "may cause fatigue or irritability",
                "recommendation": "Rest and deep breathing",
            })
        
        if not correlation:
            correlation.append({
                "metric": "overall",
                "status": "normal",
                "mood_impact": "physiological indicators support positive mood",
            })
        
        return {
            "agent": self.name,
            "correlation": correlation,
            "timestamp": datetime.now().isoformat(),
        }
