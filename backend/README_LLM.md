# LLM Integration Guide

## Quick Start

### Demo Mode (Default - No API Key)
```bash
export DEMO_MODE=true
python main.py
```

### With Gemini API
```bash
export DEMO_MODE=false
export LLM_PROVIDER=gemini
export GEMINI_API_KEY=your-key
pip install google-generativeai
python main.py
```

## Features
- Financial Hedging Agent (inspired by Globot)
- Gemini API support
- OpenAI GPT-4 support
- Mock mode (default, no API needed)
- Graceful fallback

## Does This Break the Demo?
**NO!** Demo mode is default. Everything works without API keys.

See full documentation in README_LLM.md
