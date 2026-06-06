"""
LLM Service for Lighthouse AI
Inspired by Globot's multi-agent architecture
Supports Gemini API for real-time AI agent reasoning

Author: Lighthouse AI Team
License: MIT
"""

import os
import logging
from typing import Dict, Optional
from enum import Enum

logger = logging.getLogger(__name__)


class LLMProvider(Enum):
    """Supported LLM providers"""
    GEMINI = "gemini"
    OPENAI = "openai"
    MOCK = "mock"


class LLMService:
    """
    LLM Service that supports multiple providers
    Defaults to MOCK mode for demo, can switch to real LLM with API key
    
    Usage:
        # Demo mode (default)
        llm = LLMService()
        
        # Real Gemini API
        llm = LLMService(provider="gemini", api_key="your-key")
        
        # Or via environment
        # DEMO_MODE=false
        # LLM_PROVIDER=gemini
        # GEMINI_API_KEY=your-key
    """
    
    def __init__(self, provider: str = None, api_key: str = None):
        self.demo_mode = os.getenv("DEMO_MODE", "true").lower() == "true"
        self.provider = provider or os.getenv("LLM_PROVIDER", "mock")
        self.api_key = api_key or os.getenv("GEMINI_API_KEY") or os.getenv("OPENAI_API_KEY")
        
        logger.info(f"LLMService initialized: provider={self.provider}, demo_mode={self.demo_mode}")
        
        if not self.demo_mode and not self.api_key and self.provider != "mock":
            logger.warning("No API key found for non-mock provider, falling back to mock mode")
            self.demo_mode = True
            self.provider = "mock"
    
    async def generate_agent_reasoning(
        self, 
        agent_name: str,
        crisis_context: Dict,
        temperature: float = 0.7
    ) -> Dict[str, str]:
        """
        Generate AI reasoning for a specific agent
        
        Args:
            agent_name: Name of the agent (e.g., "Financial Hedging Agent")
            crisis_context: Current crisis context with type, severity, location, etc.
            temperature: Creativity level (0-1, lower=factual, higher=creative)
        
        Returns:
            Dict with:
                - reasoning: The agent's analysis
                - confidence: Confidence level
                - recommendation: Actionable recommendation
                - risk_level: Assessed risk level
        """
        
        if self.demo_mode or self.provider == "mock":
            return self._mock_reasoning(agent_name, crisis_context)
        
        elif self.provider == "gemini":
            return await self._gemini_reasoning(agent_name, crisis_context, temperature)
        
        elif self.provider == "openai":
            return await self._openai_reasoning(agent_name, crisis_context, temperature)
        
        else:
            logger.error(f"Unknown provider: {self.provider}, falling back to mock")
            return self._mock_reasoning(agent_name, crisis_context)
    
    def _mock_reasoning(self, agent_name: str, context: Dict) -> Dict[str, str]:
        """
        Mock reasoning for demo mode
        Returns realistic-looking analysis without API calls
        """
        
        crisis_type = context.get('type', 'geopolitical')
        severity = context.get('severity', 'high')
        location = context.get('location', 'Unknown')
        
        # Agent-specific mock responses
        mock_responses = {
            "Financial Hedging Agent": {
                "reasoning": f"Analyzing financial exposure to {crisis_type} crisis in {location}. "
                           f"Currency volatility increased 15% (EUR/USD, GBP/USD). "
                           f"Commodity futures showing risk premium of 8-12%. "
                           f"Recommend hedging $2.3M exposure through currency forwards and options strategies.",
                "confidence": "High (87%)",
                "recommendation": "Execute currency hedges within 48 hours to lock in favorable rates. "
                                "Consider protective puts on oil futures.",
                "risk_level": "High"
            },
            "Market Sentiment Analyst": {
                "reasoning": f"Social media sentiment analysis shows 68% negative mentions. "
                           f"Twitter: 12.4K posts/hour with crisis keywords. "
                           f"News sentiment: -0.42 (bearish). Major outlets reporting {severity} impact.",
                "confidence": "Medium-High (75%)",
                "recommendation": "Monitor sentiment hourly. Prepare communications for stakeholder reassurance.",
                "risk_level": "Medium"
            },
            "Risk Assessment Agent": {
                "reasoning": f"Critical infrastructure analysis: 3 major shipping routes affected. "
                           f"Estimated impact: $127M in delayed shipments. "
                           f"Probability of escalation: 42% over next 72 hours.",
                "confidence": "High (82%)",
                "recommendation": "Activate contingency protocols. Reroute shipments via alternative routes. "
                                "Increase inventory buffer by 20%.",
                "risk_level": "Critical"
            },
            "Supply Chain Monitor": {
                "reasoning": f"Supply chain disruption detected in {location}. "
                           f"15 key suppliers affected. Lead time extended by 8-12 days. "
                           f"Alternative sourcing options identified in 3 regions.",
                "confidence": "High (85%)",
                "recommendation": "Contact alternative suppliers. Expedite critical shipments via air freight.",
                "risk_level": "High"
            },
            "Geopolitical Analyst": {
                "reasoning": f"Geopolitical tension index: 7.2/10 for {location}. "
                           f"Historical precedent suggests 35% chance of prolonged disruption. "
                           f"Key indicators: diplomatic activity +40%, military movements tracked.",
                "confidence": "Medium (72%)",
                "recommendation": "Engage risk mitigation strategies. Monitor diplomatic channels. "
                                "Prepare for 2-4 week disruption scenario.",
                "risk_level": "High"
            }
        }
        
        return mock_responses.get(agent_name, {
            "reasoning": f"{agent_name} analyzing {crisis_type} crisis in {location}. "
                        f"Severity level: {severity}. Monitoring key indicators and risk factors.",
            "confidence": "Medium (70%)",
            "recommendation": "Continue monitoring situation. Prepare contingency plans.",
            "risk_level": "Medium"
        })
    
    async def _gemini_reasoning(
        self, 
        agent_name: str, 
        context: Dict,
        temperature: float
    ) -> Dict[str, str]:
        """
        Real Gemini API integration
        Uses Google's Gemini model for agent reasoning
        """
        
        try:
            import google.generativeai as genai
            
            genai.configure(api_key=self.api_key)
            model = genai.GenerativeModel('gemini-pro')
            
            # Build structured prompt
            prompt = self._build_agent_prompt(agent_name, context)
            
            # Generate response
            response = model.generate_content(
                prompt,
                generation_config=genai.types.GenerationConfig(
                    temperature=temperature,
                    max_output_tokens=500,
                    top_p=0.9
                )
            )
            
            # Parse structured response
            reasoning_text = response.text
            
            return {
                "reasoning": reasoning_text,
                "confidence": "AI Generated (Gemini)",
                "recommendation": self._extract_recommendation(reasoning_text),
                "risk_level": self._assess_risk_level(reasoning_text)
            }
            
        except ImportError:
            logger.error("google-generativeai not installed. Install with: pip install google-generativeai")
            return self._mock_reasoning(agent_name, context)
        except Exception as e:
            logger.error(f"Gemini API error: {e}")
            return self._mock_reasoning(agent_name, context)
    
    async def _openai_reasoning(
        self, 
        agent_name: str, 
        context: Dict,
        temperature: float
    ) -> Dict[str, str]:
        """
        Real OpenAI API integration
        Uses GPT-4 for agent reasoning
        """
        
        try:
            import openai
            
            openai.api_key = self.api_key
            
            # Build prompt
            prompt = self._build_agent_prompt(agent_name, context)
            
            # Generate response
            response = openai.ChatCompletion.create(
                model="gpt-4",
                messages=[
                    {"role": "system", "content": f"You are {agent_name}, an AI crisis management expert."},
                    {"role": "user", "content": prompt}
                ],
                temperature=temperature,
                max_tokens=500
            )
            
            reasoning_text = response.choices[0].message.content
            
            return {
                "reasoning": reasoning_text,
                "confidence": "AI Generated (GPT-4)",
                "recommendation": self._extract_recommendation(reasoning_text),
                "risk_level": self._assess_risk_level(reasoning_text)
            }
            
        except ImportError:
            logger.error("openai not installed. Install with: pip install openai")
            return self._mock_reasoning(agent_name, context)
        except Exception as e:
            logger.error(f"OpenAI API error: {e}")
            return self._mock_reasoning(agent_name, context)
    
    def _build_agent_prompt(self, agent_name: str, context: Dict) -> str:
        """Build structured prompt for LLM"""
        
        crisis_type = context.get('type', 'Unknown')
        severity = context.get('severity', 'Unknown')
        location = context.get('location', 'Unknown')
        details = context.get('details', 'Limited information available')
        
        prompt = f"""You are {agent_name}, a specialized AI agent in a crisis management system.

CRISIS CONTEXT:
- Type: {crisis_type}
- Severity: {severity}
- Location: {location}
- Details: {details}

YOUR TASK:
Analyze this crisis from your specialized perspective and provide:
1. Your reasoning and analysis (2-3 sentences)
2. Your confidence level in this assessment
3. Specific, actionable recommendations
4. Risk level assessment (Low/Medium/High/Critical)

Be concise, professional, and focus on actionable insights."""
        
        return prompt
    
    def _extract_recommendation(self, text: str) -> str:
        """Extract recommendation from AI-generated text"""
        for line in text.split('
'):
            line_lower = line.lower()
            if any(keyword in line_lower for keyword in ['recommend', 'suggest', 'should', 'action', 'advise']):
                return line.strip()
        return "Continue monitoring and assess situation regularly"
    
    def _assess_risk_level(self, text: str) -> str:
        """Assess risk level from AI-generated text"""
        text_lower = text.lower()
        if any(word in text_lower for word in ['critical', 'severe', 'emergency', 'urgent']):
            return "Critical"
        elif any(word in text_lower for word in ['high', 'significant', 'major']):
            return "High"
        elif any(word in text_lower for word in ['moderate', 'medium']):
            return "Medium"
        else:
            return "Low"


# Singleton instance
_llm_service = None

def get_llm_service() -> LLMService:
    """
    Get or create LLM service singleton instance
    
    Returns:
        LLMService instance configured based on environment variables
    """
    global _llm_service
    if _llm_service is None:
        _llm_service = LLMService()
    return _llm_service
