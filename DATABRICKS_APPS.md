# Deploying Lighthouse AI as a Databricks App

## 📋 Prerequisites

All required files are now in place:
- ✅ `app.yaml` - App configuration
- ✅ `app.py` - Entry point for the app
- ✅ `requirements.txt` - Python dependencies (root level)
- ✅ `backend/` - Backend API code
- ✅ `frontend/` - Frontend React app (static files)

## 🚀 Deployment Steps

### Option 1: Deploy via Databricks UI

1. **Navigate to Apps**:
   - Go to your Databricks workspace
   - Click **"Compute"** → **"Apps"** in the left sidebar

2. **Create New App**:
   - Click **"Create App"**
   - Choose **"From Git Folder"** or **"From Workspace Folder"**

3. **Configure App**:
   - **Name**: `lighthouse-ai`
   - **Source**: Select this folder: `/Users/mohankoneru8@gmail.com/lighthouse-ai prototype`
   - The system will automatically detect `app.yaml`

4. **Deploy**:
   - Click **"Create"** or **"Deploy"**
   - Wait for deployment (2-5 minutes)

5. **Access**:
   - Once deployed, you'll get a URL like: `https://<workspace>.cloud.databricks.com/apps/lighthouse-ai`

### Option 2: Deploy via Databricks CLI

```bash
# Navigate to your project
cd "/Workspace/Users/mohankoneru8@gmail.com/lighthouse-ai prototype"

# Create the app
databricks apps create lighthouse-ai --source-code-path .

# Deploy the app
databricks apps deploy lighthouse-ai

# Check status
databricks apps get lighthouse-ai

# Get the app URL
databricks apps get lighthouse-ai --output json | grep url
```

## 🔧 Configuration

### Environment Variables

The app is configured with:
- `DEMO_MODE=true` - Uses mock data for demo
- `PORT=8080` - Default port for Databricks Apps

### Resources

Default resources (can be adjusted in `app.yaml`):
- **CPU**: 1 core
- **Memory**: 2 GB

To increase resources, edit `app.yaml`:
```yaml
resources:
  - name: default
    cpu: "2"          # 2 cores
    memory: "4Gi"     # 4 GB memory
```

## 📊 Architecture

```
Databricks App (Serverless)
│
├── app.py (Entry Point)
│   └── Imports backend/main.py
│
├── Backend (FastAPI)
│   ├── main.py (API Server)
│   ├── demo/crisis_sequence.py (Demo data)
│   └── SSE streaming endpoints
│
└── Frontend (Served as static files)
    ├── React Dashboard
    └── Real-time crisis timeline
```

## 🎯 Features

Once deployed, the app provides:
- ✅ **5 AI Agents** analyzing crisis scenarios
- ✅ **Real-time Timeline** with SSE streaming
- ✅ **Interactive Dashboard** with MUI components
- ✅ **Crisis Simulation** (90-second demo)
- ✅ **Risk Indicators** and recommendations

## 🔍 Testing

After deployment:

1. **Access the App URL**
2. **Click**: "🚨 Start Crisis Scenario"
3. **Watch**: Live updates from 5 AI agents
4. **Observe**: Real-time risk analysis and recommendations

## 📝 Notes

### Frontend Serving

The frontend is built as a React SPA. For Databricks Apps:
- Static files are served from `frontend/dist/` after build
- Or use the backend to serve the frontend HTML directly

To build frontend locally before deployment:
```bash
cd frontend
npm install
npm run build
```

### API Endpoints

Available at `<app-url>/`:
- `/` - Main dashboard (frontend)
- `/api/health` - Health check
- `/api/crisis/start` - Start crisis scenario
- `/api/crisis/stream` - SSE stream for timeline
- `/api/crisis/status` - Get current status

## ⚠️ Limitations

Current limitations:
- Frontend is served as static files (no hot reload)
- Demo mode only (mock data)
- Single-user session (no persistence)

## 🚀 Future Enhancements

To make it production-ready:
1. **Connect to real AI APIs** (Gemini, OpenAI)
2. **Add authentication** (Databricks OAuth)
3. **Persist data** (Unity Catalog tables)
4. **Add multi-user support** (sessions)
5. **Deploy frontend separately** (Vercel) and use CORS

## 🆘 Troubleshooting

### App fails to start
- Check logs: `databricks apps logs lighthouse-ai`
- Verify `app.yaml` syntax
- Ensure `requirements.txt` has all dependencies

### Import errors
- Verify `app.py` correctly imports from `backend/`
- Check that all Python files are in the deployed folder

### Port conflicts
- Ensure port 8080 is used (Databricks Apps default)
- Check `app.yaml` env vars match `app.py`

## 📚 Resources

- [Databricks Apps Documentation](https://docs.databricks.com/apps/)
- [FastAPI Documentation](https://fastapi.tiangolo.com/)
- [Server-Sent Events](https://developer.mozilla.org/en-US/docs/Web/API/Server-sent_events)
