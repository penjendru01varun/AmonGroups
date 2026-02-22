import os
import asyncio
import random
import json
from datetime import datetime, timedelta
from contextlib import asynccontextmanager
from typing import Dict, Any, List, Optional

from fastapi import FastAPI, WebSocket, WebSocketDisconnect, HTTPException
from fastapi.middleware.cors import CORSMiddleware
import uvicorn

from agents import (
    BaseAgent,
    OrchestratorAgent,
    VitalsAgent,
    ExerciseAgent,
    SleepAgent,
    NutritionAgent,
    CounselorAgent,
    MoodAgent,
    SocialAgent,
    AlertAgent,
    DigitalTwinAgent,
)
from core.message_bus import message_bus
from core.websocket_manager import ws_manager


orchestrator: Optional[OrchestratorAgent] = None
agents_dict: Dict[str, BaseAgent] = {}


@asynccontextmanager
async def lifespan(app: FastAPI):
    global orchestrator, agents_dict
    
    orchestrator = OrchestratorAgent()
    
    vitals_agent = VitalsAgent()
    exercise_agent = ExerciseAgent()
    sleep_agent = SleepAgent()
    nutrition_agent = NutritionAgent()
    counselor_agent = CounselorAgent()
    mood_agent = MoodAgent()
    social_agent = SocialAgent()
    alert_agent = AlertAgent()
    digital_twin_agent = DigitalTwinAgent()
    
    agents = [
        orchestrator,
        vitals_agent,
        exercise_agent,
        sleep_agent,
        nutrition_agent,
        counselor_agent,
        mood_agent,
        social_agent,
        alert_agent,
        digital_twin_agent,
    ]
    
    for agent in agents:
        await orchestrator.register_agent(agent)
        agents_dict[agent.agent_id] = agent
    
    print(f"Initialized {len(agents)} agents")
    
    yield
    
    print("Shutting down...")


app = FastAPI(
    title="MAITRI Backend",
    description="Multi-Agent AI System for Astronaut Well-Being",
    version="1.0.0",
    lifespan=lifespan,
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/")
async def root():
    return {
        "message": "MAITRI Backend is running",
        "version": "1.0.0",
        "agents_count": len(agents_dict),
    }


@app.get("/api/agents")
async def get_agents():
    """Get all registered agents with their status"""
    if orchestrator is None:
        return {"agents": [], "message": "System initializing"}
    
    result = await orchestrator.process({
        "action": "get_system_status",
    })
    
    return result


@app.get("/api/agent/{agent_id}")
async def get_agent(agent_id: str):
    """Get specific agent details"""
    if orchestrator is None:
        raise HTTPException(status_code=503, detail="System initializing")
    
    result = await orchestrator.process({
        "action": "get_agent_info",
        "agent_id": agent_id,
    })
    
    if "error" in result:
        raise HTTPException(status_code=404, detail=result["error"])
    
    return result


@app.post("/api/task")
async def create_task(task: Dict[str, Any]):
    """Create new task for orchestrator"""
    if orchestrator is None:
        raise HTTPException(status_code=503, detail="System initializing")
    
    result = await orchestrator.process({
        "action": "delegate_task",
        "task": task,
    })
    
    return result


@app.get("/api/vitals")
async def get_vitals():
    """Get current vitals"""
    if "vitals_agent" not in agents_dict:
        raise HTTPException(status_code=503, detail="System initializing")
    
    result = await agents_dict["vitals_agent"].process({
        "action": "get_current",
    })
    
    return result


@app.get("/api/vitals/history")
async def get_vitals_history(hours: int = 24):
    """Get historical vitals data"""
    return {
        "agent": "vitals_agent",
        "history": [],
        "note": "Historical data would be stored in PostgreSQL",
        "timestamp": datetime.now().isoformat(),
    }


@app.get("/api/alerts")
async def get_alerts():
    """Get recent alerts"""
    if "alert_agent" not in agents_dict:
        raise HTTPException(status_code=503, detail="System initializing")
    
    result = await agents_dict["alert_agent"].process({
        "action": "get_alerts",
        "status": "active",
    })
    
    return result


@app.post("/api/chat")
async def chat_message(message: Dict[str, Any]):
    """Send chat message to counselor agent"""
    if "counselor_agent" not in agents_dict:
        raise HTTPException(status_code=503, detail="System initializing")
    
    text = message.get("text", "")
    
    if "mood_agent" in agents_dict:
        mood_result = await agents_dict["mood_agent"].process({
            "action": "analyze_mood",
            "text": text,
        })
        emotion = mood_result.get("mood_analysis", {}).get("emotion", "neutral")
    else:
        emotion = "neutral"
    
    result = await agents_dict["counselor_agent"].process({
        "action": "chat",
        "message": text,
        "emotion": emotion,
    })
    
    return result


@app.get("/api/workout")
async def get_workout(focus: str = None):
    """Get exercise workout"""
    if "exercise_agent" not in agents_dict:
        raise HTTPException(status_code=503, detail="System initializing")
    
    result = await agents_dict["exercise_agent"].process({
        "action": "generate_workout",
        "focus": focus,
    })
    
    return result


@app.get("/api/sleep")
async def get_sleep_analysis():
    """Get sleep analysis"""
    if "sleep_agent" not in agents_dict:
        raise HTTPException(status_code=503, detail="System initializing")
    
    result = await agents_dict["sleep_agent"].process({
        "action": "analyze_sleep",
    })
    
    return result


@app.get("/api/meal-plan")
async def get_meal_plan():
    """Get meal plan"""
    if "nutrition_agent" not in agents_dict:
        raise HTTPException(status_code=503, detail="System initializing")
    
    result = await agents_dict["nutrition_agent"].process({
        "action": "generate_meal_plan",
    })
    
    return result


@app.get("/api/mood")
async def get_mood():
    """Get mood analysis"""
    if "mood_agent" not in agents_dict:
        raise HTTPException(status_code=503, detail="System initializing")
    
    result = await agents_dict["mood_agent"].process({
        "action": "get_mood_trend",
    })
    
    return result


@app.get("/api/social")
async def get_social_status():
    """Get social/morale status"""
    if "social_agent" not in agents_dict:
        raise HTTPException(status_code=503, detail="System initializing")
    
    result = await agents_dict["social_agent"].process({
        "action": "get_morale",
    })
    
    return result


@app.get("/api/prediction")
async def get_health_prediction(hours: int = 24):
    """Get health prediction"""
    if "digital_twin" not in agents_dict:
        raise HTTPException(status_code=503, detail="System initializing")
    
    result = await agents_dict["digital_twin"].process({
        "action": "predict_health",
        "hours": hours,
    })
    
    return result


@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    client_id = await ws_manager.connect(websocket)
    
    try:
        ws_manager.subscribe(client_id, "vitals")
        ws_manager.subscribe(client_id, "agents")
        ws_manager.subscribe(client_id, "alerts")
        
        await websocket.send_json({
            "type": "connected",
            "client_id": client_id,
            "message": "Connected to MAITRI",
            "timestamp": datetime.now().isoformat(),
        })
        
        vitals_task = None
        
        async def send_vitals_update():
            while True:
                if "vitals_agent" in agents_dict:
                    vitals_result = await agents_dict["vitals_agent"].process({
                        "action": "get_current",
                    })
                    
                    await ws_manager.send_personal_message({
                        "type": "vitals_update",
                        "data": vitals_result,
                        "timestamp": datetime.now().isoformat(),
                    }, client_id)
                
                await asyncio.sleep(2)
        
        vitals_task = asyncio.create_task(send_vitals_update())
        
        async def send_agent_updates():
            while True:
                if orchestrator:
                    status = await orchestrator.process({"action": "get_system_status"})
                    
                    await ws_manager.send_personal_message({
                        "type": "agent_status",
                        "data": status,
                        "timestamp": datetime.now().isoformat(),
                    }, client_id)
                
                await asyncio.sleep(5)
        
        agent_task = asyncio.create_task(send_agent_updates())
        
        while True:
            data = await ws_manager.receive_json(websocket)
            
            if not data:
                break
            
            msg_type = data.get("type", "chat")
            
            if msg_type == "chat":
                text = data.get("text", "")
                
                if "mood_agent" in agents_dict:
                    mood_result = await agents_dict["mood_agent"].process({
                        "action": "analyze_mood",
                        "text": text,
                    })
                    emotion = mood_result.get("mood_analysis", {}).get("emotion", "neutral")
                else:
                    emotion = "neutral"
                
                if "counselor_agent" in agents_dict:
                    response = await agents_dict["counselor_agent"].process({
                        "action": "chat",
                        "message": text,
                        "emotion": emotion,
                    })
                    
                    await websocket.send_json({
                        "type": "chat_response",
                        "data": response,
                        "timestamp": datetime.now().isoformat(),
                    })
                    
            elif msg_type == "command":
                if orchestrator:
                    result = await orchestrator.process({
                        "action": "handle_complex_query",
                        "query": data.get("query", ""),
                    })
                    
                    await websocket.send_json({
                        "type": "command_response",
                        "data": result,
                        "timestamp": datetime.now().isoformat(),
                    })
                    
            elif msg_type == "ping":
                await websocket.send_json({
                    "type": "pong",
                    "timestamp": datetime.now().isoformat(),
                })
                
    except WebSocketDisconnect:
        print(f"Client {client_id} disconnected")
    finally:
        if vitals_task:
            vitals_task.cancel()
        if agent_task:
            agent_task.cancel()
        ws_manager.disconnect(client_id)


async def simulate_background_tasks():
    """Background tasks for real-time simulation"""
    while True:
        await asyncio.sleep(30)
        
        if random.random() < 0.1 and "alert_agent" in agents_dict:
            event_types = ["vitals", "system", "environmental"]
            event_type = random.choice(event_types)
            
            messages = {
                "vitals": "Slight heart rate elevation detected",
                "system": "Routine system check completed",
                "environmental": "Air quality within normal parameters",
            }
            
            await agents_dict["alert_agent"].process({
                "action": "create_alert",
                "type": event_type,
                "severity": 4,
                "message": messages[event_type],
                "source": "background_monitor",
            })


@app.on_event("startup")
async def startup_event():
    asyncio.create_task(simulate_background_tasks())


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
