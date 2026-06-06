"""Crisis Sequence Timeline - Scripted Demo Events
Defines the exact timing and content of demo crisis events
"""

def get_crisis_timeline():
    """Returns the scripted crisis timeline with SSE events
    
    Returns:
        list: Timeline events with delay, type, and data
    """
    return [
        # T+0s: Alert Detection
        {
            "delay": 0,
            "type": "alert_detected",
            "data": {
                "severity": "critical",
                "title": "Geopolitical Alert Detected",
                "message": "⚠️ ALERT: Strait of Hormuz tensions escalating",
                "source": "Reuters Intelligence Feed",
                "confidence": 94,
                "risk_level": 78
            }
        },
        
        # T+2s: Market Sentinel Agent Activates
        {
            "delay": 2,
            "type": "agent_reasoning",
            "data": {
                "agent": "Market Sentinel",
                "icon": "🔭",
                "status": "analyzing",
                "steps": [
                    {
                        "step": 1,
                        "description": "Parsing Reuters intelligence feed...",
                        "status": "complete",
                        "duration": 0.8
                    },
                    {
                        "step": 2,
                        "description": "Cross-referencing Bloomberg terminals...",
                        "status": "complete",
                        "duration": 1.1
                    },
                    {
                        "step": 3,
                        "description": "Analyzing satellite imagery patterns...",
                        "status": "in_progress",
                        "duration": 0
                    }
                ],
                "sources": ["Reuters", "Bloomberg", "Maritime AIS"],
                "conclusion": "Hormuz blockade likely within 6 hours. Confidence: 94%"
            }
        },
        
        # T+5s: Risk Assessment Agent
        {
            "delay": 3,
            "type": "agent_reasoning",
            "data": {
                "agent": "Visual Risk Analyst",
                "icon": "🛰️",
                "status": "analyzing",
                "steps": [
                    {
                        "step": 1,
                        "description": "Analyzing satellite imagery of Strait of Hormuz...",
                        "status": "complete",
                        "duration": 1.2
                    },
                    {
                        "step": 2,
                        "description": "Detecting naval vessel concentrations...",
                        "status": "complete",
                        "duration": 0.9
                    },
                    {
                        "step": 3,
                        "description": "Port congestion analysis complete",
                        "status": "complete",
                        "duration": 1.0
                    }
                ],
                "sources": ["Sentinel-2", "Planet Labs", "AIS Data"],
                "conclusion": "12 naval vessels detected. Port congestion at 87%. High blockade probability."
            }
        },
        
        # T+8s: Financial Hedge Agent
        {
            "delay": 3,
            "type": "agent_reasoning",
            "data": {
                "agent": "Financial Hedge Strategist",
                "icon": "💰",
                "status": "analyzing",
                "steps": [
                    {
                        "step": 1,
                        "description": "Calculating fuel price volatility exposure...",
                        "status": "complete",
                        "duration": 0.7
                    },
                    {
                        "step": 2,
                        "description": "Modeling hedge scenarios (futures, options, swaps)...",
                        "status": "complete",
                        "duration": 1.3
                    },
                    {
                        "step": 3,
                        "description": "Optimizing hedge ratio for 3-ship fleet...",
                        "status": "complete",
                        "duration": 0.8
                    }
                ],
                "sources": ["CME Futures", "ICE Brent", "Risk Models"],
                "conclusion": "Recommend: BUY 180 Brent Dec futures @ $82.40/bbl. Hedge ratio: 67%. Expected savings: $420K"
            }
        },
        
        # T+11s: Logistics Orchestrator
        {
            "delay": 3,
            "type": "agent_reasoning",
            "data": {
                "agent": "Logistics Orchestrator",
                "icon": "🗺️",
                "status": "analyzing",
                "steps": [
                    {
                        "step": 1,
                        "description": "Calculating alternative route options...",
                        "status": "complete",
                        "duration": 0.9
                    },
                    {
                        "step": 2,
                        "description": "Analyzing Cape of Good Hope route feasibility...",
                        "status": "complete",
                        "duration": 1.1
                    },
                    {
                        "step": 3,
                        "description": "Impact assessment: fuel, time, SLA compliance...",
                        "status": "complete",
                        "duration": 1.0
                    }
                ],
                "sources": ["Maritime Routes DB", "Weather API", "Fleet Management"],
                "conclusion": "Cape route adds $180K fuel + 7 days transit. Avoids $2.1M insurance risk. Net savings: $1.92M",
                "route_data": {
                    "original": [[25.3, 56.3], [12.5, 43.3], [-15.6, 35.2]],
                    "alternative": [[25.3, 56.3], [-34.4, 18.4], [-15.6, 35.2]]
                }
            }
        },
        
        # T+15s: Adversarial Debate Begins
        {
            "delay": 4,
            "type": "debate_start",
            "data": {
                "red_team": {
                    "agent": "Red Team (Risk Averse)",
                    "icon": "🔴",
                    "argument": "Rerouting via Cape adds $180K fuel cost plus 7-day delay. This breaches client SLA (delivery window: 14 days). Breach penalty: $340K. Total cost: $520K. Risk of reputation damage.",
                    "confidence": 67,
                    "supporting_data": [
                        "Contract SLA: 14-day delivery window",
                        "Current transit time: 12 days (Hormuz route)",
                        "Alternative transit time: 19 days (Cape route)",
                        "SLA breach penalty: $340K"
                    ]
                },
                "blue_team": {
                    "agent": "Blue Team (Opportunity Seeker)",
                    "icon": "🔵",
                    "argument": "Cape route avoids $2.1M war risk insurance premium increase. Even with 7-day delay, we can negotiate SLA extension citing force majeure (geopolitical crisis). Net savings: $1.92M after fuel costs.",
                    "confidence": 89,
                    "supporting_data": [
                        "War risk insurance increase: $2.1M (Hormuz blockade)",
                        "Additional fuel cost: $180K (Cape route)",
                        "Force majeure clause: Applicable for geopolitical events",
                        "Net savings: $1.92M"
                    ]
                }
            }
        },
        
        # T+19s: Financial Impact Update
        {
            "delay": 4,
            "type": "financial_update",
            "data": {
                "original_cost": 2340000,
                "fuel_premium": 180000,
                "insurance_savings": -2100000,
                "net_savings": 1920000,
                "hedge_recommendation": {
                    "action": "BUY",
                    "instrument": "Brent Crude Dec Futures",
                    "contracts": 180,
                    "entry_price": 82.40,
                    "target_price": 85.20,
                    "expected_gain": 420000
                }
            }
        },
        
        # T+22s: Consensus Reached
        {
            "delay": 3,
            "type": "debate_verdict",
            "data": {
                "winner": "blue_team",
                "reason": "Blue Team confidence (89%) exceeds Red Team (67%). Financial analysis favors Cape route with $1.92M net savings.",
                "final_recommendation": {
                    "action": "REROUTE",
                    "route": "Cape of Good Hope",
                    "ships_affected": 3,
                    "execute_hedge": True,
                    "notify_clients": True,
                    "estimated_savings": 1920000
                }
            }
        },
        
        # T+25s: Human-in-the-Loop Prompt
        {
            "delay": 3,
            "type": "hitl_prompt",
            "data": {
                "title": "Decision Approval Required",
                "message": "AI agents recommend rerouting 3 vessels via Cape of Good Hope. Approve to execute?",
                "recommendation": {
                    "action": "Reroute + Hedge",
                    "confidence": 89,
                    "financial_impact": "+$1.92M savings",
                    "risk_reduction": "87%",
                    "execution_time": "Immediate"
                },
                "options": [
                    {"id": "approve", "label": "Approve & Execute", "style": "primary"},
                    {"id": "modify", "label": "Modify Plan", "style": "secondary"},
                    {"id": "reject", "label": "Reject", "style": "danger"}
                ]
            }
        }
    ]


def get_resolution_sequence():
    """Timeline for post-approval resolution animation"""
    return [
        {
            "delay": 0,
            "type": "execution_start",
            "data": {"message": "Executing decision..."}
        },
        {
            "delay": 1,
            "type": "route_update",
            "data": {
                "ships_rerouted": 3,
                "new_route": "Cape of Good Hope",
                "route_coordinates": [[25.3, 56.3], [-34.4, 18.4], [-15.6, 35.2]]
            }
        },
        {
            "delay": 2,
            "type": "hedge_executed",
            "data": {
                "contracts_purchased": 180,
                "instrument": "Brent Dec Futures",
                "entry_price": 82.40
            }
        },
        {
            "delay": 3,
            "type": "crisis_resolved",
            "data": {
                "status": "Crisis Contained",
                "total_savings": 1920000,
                "risk_level": 22,
                "message": "🎉 Crisis successfully mitigated. All ships rerouted safely."
            }
        }
    ]