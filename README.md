# 🌐 Lighthouse AI - Crisis Management Platform

**Transform geopolitical chaos into actionable intelligence in 90 seconds.**

Lighthouse AI is an AI-powered crisis management system featuring a 5-agent architecture that monitors global risks, analyzes financial impact, and orchestrates real-time responses to maritime crises.

## 🎯 Key Features

* **🚨 Real-Time Crisis Detection**: Instant alerts for geopolitical threats (Strait of Hormuz blockade scenario)
* **🤖 5-Agent AI System**: Market Sentinel, Visual Risk Analyst, Financial Hedge Strategist, Logistics Orchestrator, Adversarial Debate
* **💰 Animated Financial Impact**: Live cost tracking with $1.92M savings visualization
* **⚔️ Red vs Blue Adversarial Debate**: Transparent decision-making process
* **🗺️ Route Optimization**: Automatic rerouting with animated map transitions
* **🎭 Human-in-the-Loop**: Final approval control for critical decisions
* **📊 SSE Streaming**: Real-time agent reasoning display

---

## 🚀 Quick Start (2-Hour Sprint Setup)

### Prerequisites

* **Python 3.9+**
* **Node.js 18+** and **pnpm** (or npm)
* **Git**

### Installation

```bash
# 1. Navigate to the project directory
cd lighthouse-ai

# 2. Backend Setup
cd backend
pip install -r requirements.txt
cd ..

# 3. Frontend Setup
cd frontend
pnpm install  # or: npm install
cd ..
```

### Running the Application

**Terminal 1 - Backend:**
```bash
cd backend
export DEMO_MODE=true  # Use mock data
python main.py
# Backend will start at http://localhost:8000
```

**Terminal 2 - Frontend:**
```bash
cd frontend
pnpm dev  # or: npm run dev
# Frontend will open at http://localhost:3000
```

### Access the App

Open your browser to `http://localhost:3000` and click **"🚨 Start Crisis Scenario"**

---

## 🎬 Demo Script (90-Second Hackathon Pitch)

### Timing Breakdown

| Time | Action | What Audience Sees |
|------|--------|--------------------|
| **0:00** | Open dashboard | Calm green dashboard, 3 ships tracked, risk level: 35 |
| **0:15** | Click "Start Scenario" | ⚠️ Alert bar slides down: "Geopolitical Alert Detected" |
| **0:20** | Agents activate | 5 agent cards appear with typewriter reasoning |
| **0:40** | Financial analysis | Animated cost counter: $180K fuel + $2.1M savings |
| **0:55** | Debate begins | Red vs Blue panels animate in with arguments |
| **1:10** | Verdict reached | Blue Team wins (89% confidence), recommendation glows |
| **1:15** | HITL prompt appears | "Approve & Execute" button pulses |
| **1:20** | Click Approve | 🎉 Green sweep, ships reroute, savings counter animates |
| **1:30** | Resolution | "Crisis Contained" badge, $1.92M savings displayed |

### Key Talking Points

1. **"Watch AI Think in Real-Time"** — Point to agent reasoning cards
2. **"Adversarial Debate Ensures Quality"** — Highlight Red vs Blue confidence scores
3. **"Human Always in Control"** — Emphasize the approval button
4. **"$1.92M Saved Automatically"** — Financial impact is the hero metric

---

## 🏗️ Architecture

### Backend (FastAPI)

```
backend/
├── main.py                 # FastAPI server + SSE endpoints
├── demo/
│   └── crisis_sequence.py  # Scripted timeline (25s of events)
├── core/
│   └── reasoning_schemas.py # Agent reasoning structures
└── services/               # Mock services (market, satellite, etc.)
```

### Frontend (React + Vite + MUI)

```
frontend/src/
├── App.jsx                      # MUI theme + Crisis provider
├── main.jsx                     # Entry point
├── components/
│   ├── CrisisOverlay.jsx        # Main crisis UI overlay
│   ├── AgentThinkingCard.jsx   # Agent reasoning visualization
│   ├── DebatePanel.jsx          # Red vs Blue debate UI
│   └── FinancialImpactWidget.jsx # Animated cost ticker
├── context/
│   └── CrisisContext.jsx        # Crisis state machine
└── pages/
    └── Dashboard.jsx            # Main dashboard page
```

### State Machine

```
NORMAL → ALERT_DETECTED → AGENTS_REASONING → DEBATE → AWAITING_APPROVAL → RESOLVED
```

---

## 🌐 How it works in production

The **"Start Crisis Scenario"** button is a demo affordance. In a real deployment **no human clicks it** — the crisis pipeline is event-driven from continuous data ingestion. This section documents the production architecture and points at the specific files that change as you move from scripted demo to live data.

### Trigger sources (any can fire the pipeline)

| Source | Mechanism | Latency | Example |
| --- | --- | --- | --- |
| **Push from a data provider** | Webhook → POST endpoint | seconds | Reuters/Bloomberg sends a "Strait of Hormuz tension" story to `POST /webhooks/reuters` |
| **Streaming feed** | Kafka / Pub/Sub / Kinesis consumer | sub-second | AIS vessel-tracking stream emits a "vessel diverted" event |
| **Polling job** | Cron / Airflow / Temporal worker | 30 s – 5 min | Every minute query MarineTraffic API; flag if N vessels stop in a chokepoint |
| **Threshold alarm** | Time-series rule engine (Datadog / Prometheus / custom) | seconds | Brent crude futures move > 3% in 15 minutes |
| **Image diff job** | Periodic satellite-tile pull → vision model → diff vs baseline | minutes | Sentinel-2 tiles show 12+ naval vessels in a chokepoint vs baseline |
| **Operator override** | UI button (the only path you have today) | — | NOC manager manually triggers based on private intel |

### Production flow

```
                 ┌─────────────────────────────────────────────┐
 (1) ingest   →  │  Reuters · Bloomberg · AIS · Sentinel-2 ·   │
                 │  CME · Insurance markets · Sanction lists   │
                 └───────────────────┬─────────────────────────┘
                                     │  push or pull
                                     ▼
 (2) detect   →  ┌─────────────────────────────────────────────┐
                 │  Detector(s): rules + small ML models       │
                 │  Output: typed `crisis_alert` event with    │
                 │  severity, location, affected_assets        │
                 └───────────────────┬─────────────────────────┘
                                     │  publish
                                     ▼
 (3) bus      →  ┌─────────────────────────────────────────────┐
                 │  Event broker (Kafka / Pub-Sub)             │
                 │  topic: `crisis.alerts`                     │
                 └───────────────────┬─────────────────────────┘
                                     │  fan-out
                                     ▼
 (4) orchestr →  ┌─────────────────────────────────────────────┐
                 │  Crisis orchestrator (LangGraph / Temporal /│
                 │  CrewAI / custom asyncio).  Spawns the 5    │
                 │  agents in parallel; collects partial       │
                 │  results; runs adversarial debate; emits a  │
                 │  recommendation.                            │
                 └───────────────────┬─────────────────────────┘
                                     │  emits step events
        ┌────────────────────────────┼────────────────────────────┐
        ▼                            ▼                            ▼
 (5a) UI push           (5b) ops integrations        (5c) durable store
 SSE / WebSocket to    Slack · PagerDuty · Email ·   Postgres + S3
 ops dashboards (the   Mobile push · ServiceNow      audit trail of every
 only path today)      ticket                        agent step, tool call,
                                                     decision
                                     │
                                     ▼
 (6) HITL     →  Decision approval (the "Approve & Execute" button) routed
                 by policy (e.g. > $1M decisions → COO; otherwise → NOC).
                                     │
                                     ▼
 (7) execute  →  Trading API places hedge · Fleet management API reroutes ·
                 Insurance broker API amends war-risk cover · Twilio /
                 SendGrid notifies clients · ERP updated.
```

### Mapping to this codebase

The repo today implements only steps **(4)** orchestrate, **(5a)** UI push, and **(6)** HITL — and step (4) is scripted. The production path is:

1. **Replace** `POST /api/demo/trigger-crisis` in `backend/main.py` with passive ingest endpoints / consumers — e.g. `POST /webhooks/reuters` (signed by provider), an `asyncio` Kafka consumer, and a Temporal/cron worker that polls feeds. All of them emit a normalized `CrisisAlert` event. The current demo button becomes one debug ingress among many.

2. **Add a detection layer** under `backend/detection/` that classifies raw signals into typed `CrisisAlert`s with `severity`, `location`, and `affected_assets`. This is what populates the `crisis_context` dict that today is hardcoded as `HORMUZ_CRISIS_CONTEXT` in `backend/main.py`.

3. **Replace** `crisis_sequence.get_crisis_timeline()` with a real orchestrator that runs the 5 agents in parallel (`asyncio.gather`). The Financial Hedge Strategist on the [`feature/llm_integration`](#) branch is a worked example: a Claude-skill-driven LLM agent backed by deterministic calculator tools (`backend/claude_skill/financial_hedging/`).

4. **Persist everything** to Postgres (incidents, decisions, audit log) + S3 (raw evidence: news payloads, satellite tiles, agent traces). Today agent output exists only as transient SSE events.

5. **Multi-tenant fan-out.** Replace the 1:1 `EventSource` with WebSocket / Redis pub-sub (or a managed service like Pusher/Ably) so the same alert reaches every subscriber with policy interest.

6. **Policy-routed HITL.** The `/api/decision/approve` endpoint should consult an approval policy (decision threshold, role, geography, etc.) and route via Slack/mobile push to the right approver — not just accept any caller.

7. **Execution integrations.** Today `/api/decision/approve` just returns success. In production, approval triggers real side-effects: trading API to place the hedge, fleet management (e.g. Veson IMOS) to update voyage plans, insurance broker to amend war-risk cover, and customer notifications via Twilio / SendGrid.

### The single line that captures the shift

```python
# backend/main.py — crisis_event_generator()
from demo.crisis_sequence import get_crisis_timeline
timeline = get_crisis_timeline()        # ← scripted today

# In production:
# timeline = await orchestrator.handle(alert)   # alert came from step (3)
```

Everything **downstream** of that line — the SSE event shape, the `LIVE`/`DEMO` provenance chip, the `AgentThinkingCard` schema, the HITL approve flow — stays the same. The wire format and UI are already production-correct; only the *source* of agent reasoning needs to change from script → orchestrator.

---

## 🎨 "Wow Moments" Checklist

* ✅ **Crisis Alarm**: Screen pulses red when alert triggers
* ✅ **Visible AI Thinking**: 5 agents reason with typewriter animation
* ✅ **Live Financial Counter**: Numbers animate from $2.3M → $1.92M savings
* ✅ **Adversarial Debate**: Red vs Blue panels with confidence bars
* ✅ **Human Moment**: Glowing "Approve & Execute" button
* ✅ **Resolution Animation**: Green sweep + "Crisis Contained" badge

---

## 🛠️ Configuration

### Backend `.env` (Optional)

```bash
DEMO_MODE=true              # Use mock data (recommended for hackathon)
PORT=8000                   # Backend port
GOOGLE_API_KEY=your_key     # For real Gemini API (future enhancement)
```

### Frontend Environment

* API endpoint is hardcoded to `http://localhost:8000`
* Modify `CrisisContext.jsx` to change backend URL

---

## 🔧 Customization

### Adjust Crisis Timeline Speed

Edit `backend/demo/crisis_sequence.py` and modify `delay` values:

```python
{
    "delay": 2,  # Change this (seconds between events)
    "type": "agent_reasoning",
    ...
}
```

### Change Crisis Scenario

Modify event data in `crisis_sequence.py` to create new scenarios (e.g., Panama Canal disruption, Arctic route crisis)

### Add Real Gemini API

1. Install: `pip install google-generativeai`
2. Set `DEMO_MODE=false` in `.env`
3. Add `GOOGLE_API_KEY` to `.env`
4. Implement real API calls in `backend/services/llm_service.py`

---

## 📦 Tech Stack

**Backend:**
* FastAPI (async web framework)
* SSE (Server-Sent Events) for real-time streaming
* Pydantic (data validation)

**Frontend:**
* React 18 + Vite
* Material-UI (MUI) for components
* CSS keyframe animations
* EventSource for SSE client

**AI (Future):**
* Google Gemini 3.0
* CrewAI multi-agent framework
* OpenAI-compatible APIs

---

## 🐛 Troubleshooting

### Backend won't start
* Check Python version: `python --version` (need 3.9+)
* Install dependencies: `pip install -r requirements.txt`
* Check port 8000 is free: `lsof -i :8000`

### Frontend won't start
* Check Node version: `node --version` (need 18+)
* Delete `node_modules` and reinstall: `rm -rf node_modules && pnpm install`
* Check port 3000 is free: `lsof -i :3000`

### Crisis doesn't trigger
* Open browser console (F12) and check for errors
* Verify backend is running: visit `http://localhost:8000`
* Check CORS: backend should allow frontend origin

### SSE connection fails
* Check `http://localhost:8000/api/demo/crisis-stream` in browser
* Ensure `Access-Control-Allow-Origin: *` header is set
* Try disabling browser extensions (ad blockers can break SSE)

---

## 🎯 Hackathon Tips

1. **Rehearse 3 Times**: Practice the demo flow until you can do it in your sleep
2. **Have a Backup**: Record a video in case WiFi fails
3. **Start with Impact**: "We saved $1.92M in 90 seconds" is your opening line
4. **Show the Agents**: Pan to agent reasoning cards — this is the differentiator
5. **End with Vision**: "Imagine this for every crisis, everywhere, always"

---

## 📄 License

MIT License - Feel free to use, modify, and distribute

---

## 👥 Credits

Built with inspiration from Globot Shield and enhanced with:
* Real-time SSE streaming
* Adversarial debate visualization
* Animated financial impact tracking
* Human-in-the-loop decision approval

---

## 🚀 Next Steps (Post-Hackathon)

* [ ] Integrate real Gemini 3.0 API
* [ ] Add Deck.gl map with animated ship routes
* [ ] Connect to live AIS maritime data
* [ ] Implement PostgreSQL for crisis history
* [ ] Add user authentication (Clerk)
* [ ] Deploy to cloud (Vercel + Railway)
* [ ] Create mobile app version

---

**Ready to impress the judges? Click that red button and watch the magic happen! 🎉**