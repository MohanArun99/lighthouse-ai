"""
Lighthouse AI - Databricks App Entry Point
Crisis Management & Risk Intelligence Platform

This is the main entry point for the Databricks App.
It imports and exposes the FastAPI application from the backend.
"""

import os
import sys

# Add backend to Python path
backend_path = os.path.join(os.path.dirname(__file__), 'backend')
sys.path.insert(0, backend_path)

# Import the FastAPI app from backend
from main import app

# Set environment variables
os.environ.setdefault('DEMO_MODE', 'true')
os.environ.setdefault('PORT', '8080')

# Export the app for Uvicorn
__all__ = ['app']

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        app, 
        host="0.0.0.0", 
        port=int(os.environ.get("PORT", 8080)),
        log_level="info"
    )
