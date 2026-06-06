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