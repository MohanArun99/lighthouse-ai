"""Lighthouse AI - FastAPI Backend Server
Enhanced crisis management system with SSE streaming
"""
import asyncio
import json
from datetime import datetime
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import StreamingResponse
from pydantic import BaseModel
from typing import Optional, Dict, Any
import os

# Initialize FastAPI app
app = FastAPI(
    title="Lighthouse AI",
    description="Crisis Management & Risk Intelligence Platform",
    version="2.0.0"
)

# CORS configuration for development
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Configure appropriately for production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Demo mode flag
DEMO_MODE = os.getenv("DEMO_MODE", "true").lower() == "true"


class CrisisScenario(BaseModel):
    """Crisis scenario configuration"""
    scenario_type: str = "hormuz_blockade"
    auto_trigger: bool = True
    speed_multiplier: float = 1.0


@app.get("/")
async def root():
    """Health check endpoint"""
    return {
        "service": "Lighthouse AI",
        "status": "operational",
        "demo_mode": DEMO_MODE,
        "timestamp": datetime.utcnow().isoformat()
    }


@app.get("/api/status")
async def get_status():
    """System status endpoint"""
    return {
        "ships_tracked": 3,
        "risk_level": 35,
        "active_alerts": 0,
        "agents_active": 5,
        "last_update": datetime.utcnow().isoformat()
    }


@app.post("/api/demo/trigger-crisis")
async def trigger_crisis(scenario: CrisisScenario):
    """Trigger a demo crisis scenario"""
    return {
        "success": True,
        "scenario": scenario.scenario_type,
        "message": "Crisis scenario initiated",
        "stream_endpoint": "/api/demo/crisis-stream"
    }


async def crisis_event_generator():
    """Generate SSE events for crisis sequence"""
    from demo.crisis_sequence import get_crisis_timeline
    
    timeline = get_crisis_timeline()
    
    for event in timeline:
        # Wait for the specified delay
        await asyncio.sleep(event["delay"])
        
        # Send SSE event
        event_data = {
            "timestamp": datetime.utcnow().isoformat(),
            "type": event["type"],
            "data": event["data"]
        }
        
        yield f"data: {json.dumps(event_data)}\n\n"
    
    # Send completion event
    yield f"data: {json.dumps({'type': 'complete', 'message': 'Crisis sequence complete'})}\n\n"


@app.get("/api/demo/crisis-stream")
async def crisis_stream():
    """SSE endpoint for crisis event streaming"""
    return StreamingResponse(
        crisis_event_generator(),
        media_type="text/event-stream",
        headers={
            "Cache-Control": "no-cache",
            "Connection": "keep-alive",
            "X-Accel-Buffering": "no"
        }
    )


@app.post("/api/decision/approve")
async def approve_decision(decision: Dict[str, Any]):
    """Approve and execute a crisis decision"""
    return {
        "success": True,
        "decision_id": decision.get("id"),
        "status": "executed",
        "message": "Decision approved and executed successfully",
        "execution_time": datetime.utcnow().isoformat()
    }


@app.post("/api/demo/reset")
async def reset_demo():
    """Reset demo to initial state"""
    return {
        "success": True,
        "message": "Demo reset to initial state",
        "status": "normal"
    }


if __name__ == "__main__":
    import uvicorn
    port = int(os.getenv("PORT", "8000"))
    uvicorn.run(app, host="0.0.0.0", port=port, log_level="info")