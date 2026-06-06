"""Lighthouse AI - FastAPI Backend Server
Enhanced crisis management system with SSE streaming
"""
import asyncio
import json
import logging
from datetime import datetime
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import StreamingResponse
from pydantic import BaseModel
from typing import Optional, Dict, Any
import os

logger = logging.getLogger(__name__)

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


# Comma-separated agent names that should be served by a live LLM instead of
# the scripted timeline. Anything not in this set still uses the mock card,
# so toggling individual agents is safe.
LIVE_AGENTS = {
    name.strip()
    for name in os.getenv("LIVE_AGENTS", "").split(",")
    if name.strip()
}

# Per-agent live timeout. Demo continues with the scripted card on timeout.
LIVE_AGENT_TIMEOUT_S = float(os.getenv("LIVE_AGENT_TIMEOUT_S", "12"))


# Hormuz crisis context shared with live agents. Kept in code so the SSE path
# stays self-contained; richer context can be threaded later from the alert
# event itself.
HORMUZ_CRISIS_CONTEXT: Dict[str, Any] = {
    "type": "geopolitical",
    "severity": "high",
    "location": "Strait of Hormuz",
    "scenario": "hormuz_blockade",
    "ships_affected": 3,
    "fuel_exposure_tons": 6000,
    "fuel_spot_price_usd_per_ton": 650,
    "fx_exposure_eur": 8_000_000,
    "fx_rate_eur_usd": 1.08,
    "war_risk_premium_increase_usd": 2_100_000,
    "expected_horizon_days": 180,
    "annualised_fuel_volatility": 0.28,
    "spot_futures_correlation": 0.92,
}


async def _maybe_live_agent_card(
    scripted_data: Dict[str, Any],
) -> Dict[str, Any]:
    """Return a live LLM-generated card for ``scripted_data['agent']`` if the
    agent is enabled via ``LIVE_AGENTS``; otherwise return ``scripted_data``
    unchanged. On any failure fall back to ``scripted_data`` so the demo
    timeline always completes.
    """
    agent_name = scripted_data.get("agent")
    if not agent_name or agent_name not in LIVE_AGENTS:
        return scripted_data

    if agent_name == "Financial Hedge Strategist":
        try:
            from services.financial_hedge_skill_agent import (
                generate_financial_hedge_card,
            )
        except Exception as exc:
            logger.warning("financial_hedge live agent import failed: %s", exc)
            return scripted_data

        try:
            live_card = await asyncio.wait_for(
                generate_financial_hedge_card(
                    crisis_context=HORMUZ_CRISIS_CONTEXT,
                    scripted_card=scripted_data,
                ),
                timeout=LIVE_AGENT_TIMEOUT_S,
            )
            return live_card
        except asyncio.TimeoutError:
            logger.warning(
                "financial_hedge live agent timed out after %.1fs; using scripted card",
                LIVE_AGENT_TIMEOUT_S,
            )
            return scripted_data
        except Exception as exc:
            logger.warning(
                "financial_hedge live agent failed (%s); using scripted card",
                exc,
            )
            return scripted_data

    return scripted_data


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
        await asyncio.sleep(event["delay"])

        data = event["data"]
        if event["type"] == "agent_reasoning":
            data = await _maybe_live_agent_card(data)

        event_data = {
            "timestamp": datetime.utcnow().isoformat(),
            "type": event["type"],
            "data": data,
        }

        yield f"data: {json.dumps(event_data)}\n\n"

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