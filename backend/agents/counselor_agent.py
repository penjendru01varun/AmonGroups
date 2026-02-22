import random
from datetime import datetime
from typing import Dict, Any, List
from .base_agent import BaseAgent


class CounselorAgent(BaseAgent):
    """Provides psychological support with CBT techniques"""

    def __init__(self, agent_id: str = None):
        super().__init__(
            agent_id=agent_id or "counselor_agent",
            name="Psychological Counselor",
            agent_type="psychological",
            capabilities=[
                "emotional_support",
                "cbt_techniques",
                "stress_management",
                "motivational_coaching",
                "crisis_intervention",
            ],
        )
        
        self.conversation_history = []
        
        self.intervention_strategies = {
            "anxiety": [
                "Let's try the 4-7-8 breathing: Inhale 4s, hold 7s, exhale 8s.",
                "Name 5 things you can see, 4 you can touch, 3 you can hear.",
                "Progressive muscle relaxation: Start with toes, tense and release.",
            ],
            "loneliness": [
                "Would you like me to help compose a message to your family?",
                "The crew is here for you. Shall I check if anyone's free for a call?",
                "Remember, thousands of people on Earth are supporting this mission.",
            ],
            "stress": [
                "Take a 5-minute break to view Earth from the Cupola.",
                "I've queued your favorite relaxing music.",
                "Let's break down what's overwhelming into smaller steps.",
            ],
            "sadness": [
                "It's okay to feel sad. Even astronauts have emotional days.",
                "Would you like to talk about what's on your mind?",
                "Shall I share some memories from your loved ones?",
            ],
            "homesickness": [
                "Missing home is natural. You're making incredible sacrifice.",
                "I've prepared a photo slideshow of Earth locations.",
                "Would you like to write in your journal? I can help.",
            ],
            "motivation": [
                "Remember why you're here - you're making history!",
                "Let's break your next task into smaller, achievable steps.",
                "You've overcome so much to get here. You're capable.",
            ],
        }
        
        self.cbt_techniques = {
            "cognitive_restructuring": [
                "What evidence supports this thought? What contradicts it?",
                "Is this a fact or an interpretation?",
                "What would you tell a friend in this situation?",
            ],
            "behavioral_activation": [
                "Let's schedule a small enjoyable activity.",
                "Even small accomplishments matter - let's celebrate wins.",
                "Movement helps mood - shall we do a quick stretch?",
            ],
            "mindfulness": [
                "Focus on your breath for 2 minutes - just observe thoughts.",
                "Ground yourself: feel your feet, your seat, the air.",
                "Notice 3 sounds around you right now.",
            ],
        }

    async def process(self, input_data: Dict[str, Any]) -> Dict[str, Any]:
        """Process counseling request"""
        action = input_data.get("action", "chat")
        
        if action == "chat":
            return await self._generate_response(input_data)
        elif action == "check_in":
            return await self._daily_check_in()
        elif action == "wellbeing_assessment":
            return await self._assess_wellbeing()
        elif action == "cbt_session":
            return await self._cbt_session(input_data)
        else:
            return {"error": f"Unknown action: {action}"}

    async def _generate_response(self, data: Dict) -> Dict[str, Any]:
        """Generate empathetic response based on detected emotion"""
        message = data.get("message", "")
        emotion = data.get("emotion", "neutral")
        
        message_lower = message.lower()
        
        concern = self._detect_concern(message_lower)
        
        interventions = self.intervention_strategies.get(concern, self.intervention_strategies["stress"])
        intervention = random.choice(interventions)
        
        empathy_phrases = {
            "anxiety": "I hear that you're feeling anxious. That's completely normal in space.",
            "loneliness": "It sounds like you're feeling alone. Even in space, you're never truly isolated.",
            "stress": "I understand you're under pressure. Let's find a way to ease it.",
            "sadness": "It's okay to feel sad sometimes. Your feelings are valid.",
            "homesickness": "Missing home shows how much you care. That's beautiful.",
            "motivation": "It's okay to have low moments. You're incredibly strong.",
            "general": "I'm here to listen and support you.",
        }
        
        empathy = empathy_phrases.get(concern, empathy_phrases["general"])
        
        response_text = f"{empathy} {intervention}"
        
        conversation_entry = {
            "timestamp": datetime.now().isoformat(),
            "user_message": message,
            "ai_response": response_text,
            "detected_concern": concern,
            "emotion": emotion,
        }
        
        self.conversation_history.append(conversation_entry)
        
        crisis_detected = self._check_for_crisis(message_lower)
        
        if crisis_detected:
            self.update_status("alert")
            await self.send_message("alert_agent", {
                "type": "psychological_emergency",
                "message": message,
                "emotion": emotion,
                "severity": "critical",
            })
        
        self.update_status("idle")
        
        return {
            "agent": self.name,
            "response": response_text,
            "detected_concern": concern,
            "emotion": emotion,
            "intervention_type": intervention,
            "crisis_detected": crisis_detected,
            "timestamp": datetime.now().isoformat(),
        }

    def _detect_concern(self, message: str) -> str:
        """Detect primary concern from message"""
        keywords = {
            "anxiety": ["anxious", "nervous", "worry", "scared", "afraid", "panic"],
            "loneliness": ["lonely", "alone", "isolated", "miss", "no one"],
            "stress": ["stress", "overwhelm", "pressure", "too much", "burnout"],
            "sadness": ["sad", "down", "depressed", "unhappy", "cry", "tears"],
            "homesickness": ["home", "family", "earth", "miss home", "loved ones"],
            "motivation": ["tired", "exhausted", "no energy", "can't", "give up"],
        }
        
        for concern, words in keywords.items():
            if any(word in message for word in words):
                return concern
        
        return "general"

    def _check_for_crisis(self, message: str) -> bool:
        """Check for crisis keywords"""
        crisis_keywords = ["hurt myself", "end it", "die", "suicide", "kill myself", "want to die"]
        return any(keyword in message for keyword in crisis_keywords)

    async def _daily_check_in(self) -> Dict[str, Any]:
        """Daily psychological check-in"""
        return {
            "agent": self.name,
            "check_in": {
                "questions": [
                    "How would you rate your mood today? (1-10)",
                    "Have you experienced any anxiety or stress?",
                    "How well did you sleep last night?",
                    "Do you feel connected to your team?",
                    "Is there anything specific worrying you?",
                ],
                "purpose": "Daily mental health monitoring",
                "estimated_time": "5 minutes",
                "best_time": "After morning routine",
            },
            "timestamp": datetime.now().isoformat(),
        }

    async def _assess_wellbeing(self) -> Dict[str, Any]:
        """Assess overall psychological wellbeing"""
        if not self.conversation_history:
            return {
                "agent": self.name,
                "status": "insufficient_data",
                "timestamp": datetime.now().isoformat(),
            }
        
        recent = self.conversation_history[-20:]
        
        concern_counts = {}
        for entry in recent:
            concern = entry.get("detected_concern", "general")
            concern_counts[concern] = concern_counts.get(concern, 0) + 1
        
        wellbeing_score = 7.0
        
        negative_concerns = ["anxiety", "stress", "sadness", "loneliness"]
        for concern, count in concern_counts.items():
            if concern in negative_concerns:
                wellbeing_score -= count * 0.2
        
        wellbeing_score = max(1, min(10, wellbeing_score))
        
        return {
            "agent": self.name,
            "wellbeing_score": round(wellbeing_score, 1),
            "emotional_profile": concern_counts,
            "dominant_concern": max(concern_counts, key=concern_counts.get) if concern_counts else "general",
            "needs_attention": wellbeing_score < 5,
            "recommendations": self._generate_recommendations(wellbeing_score),
            "timestamp": datetime.now().isoformat(),
        }

    def _generate_recommendations(self, score: float) -> List[str]:
        """Generate wellbeing recommendations"""
        if score < 5:
            return [
                "Schedule video call with mission psychologist",
                "Increase physical exercise routine",
                "Practice mindfulness 10 minutes, 3x daily",
                "Connect with crew members",
            ]
        elif score < 7:
            return [
                "Continue daily mood tracking",
                "Try a new hobby or activity",
                "Connect with different crew members",
            ]
        else:
            return [
                "Maintain current healthy habits",
                "Share positive experiences with team",
                "Consider mentoring newer astronauts",
            ]

    async def _cbt_session(self, data: Dict) -> Dict[str, Any]:
        """Run a CBT session"""
        thought = data.get("thought", "")
        
        technique = random.choice(list(self.cbt_techniques.keys()))
        questions = self.cbt_techniques[technique]
        
        return {
            "agent": self.name,
            "cbt_session": {
                "technique": technique.replace("_", " ").title(),
                "your_thought": thought,
                "questions": questions,
                "goal": "Examine and reframe negative thought patterns",
            },
            "timestamp": datetime.now().isoformat(),
        }
