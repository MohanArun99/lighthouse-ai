import React, { createContext, useContext, useState, useCallback } from 'react';

/**
 * Crisis State Machine
 * NORMAL → ALERT_DETECTED → AGENTS_REASONING → DEBATE → AWAITING_APPROVAL → RESOLVED
 */
const CRISIS_STATES = {
  NORMAL: 'NORMAL',
  ALERT_DETECTED: 'ALERT_DETECTED',
  AGENTS_REASONING: 'AGENTS_REASONING',
  DEBATE: 'DEBATE',
  AWAITING_APPROVAL: 'AWAITING_APPROVAL',
  RESOLVED: 'RESOLVED',
};

const CrisisContext = createContext();

export const useCrisis = () => {
  const context = useContext(CrisisContext);
  if (!context) {
    throw new Error('useCrisis must be used within CrisisProvider');
  }
  return context;
};

export const CrisisProvider = ({ children }) => {
  const [state, setState] = useState(CRISIS_STATES.NORMAL);
  const [alert, setAlert] = useState(null);
  const [agents, setAgents] = useState([]);
  const [debate, setDebate] = useState(null);
  const [financialData, setFinancialData] = useState(null);
  const [recommendation, setRecommendation] = useState(null);
  const [eventSource, setEventSource] = useState(null);

  const startCrisis = useCallback(async () => {
    // Trigger crisis on backend
    try {
      const response = await fetch('http://localhost:8000/api/demo/trigger-crisis', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          scenario_type: 'hormuz_blockade',
          auto_trigger: true,
          speed_multiplier: 1.0,
        }),
      });

      if (!response.ok) throw new Error('Failed to trigger crisis');

      // Open SSE connection
      const es = new EventSource('http://localhost:8000/api/demo/crisis-stream');
      setEventSource(es);

      es.onmessage = (event) => {
        const data = JSON.parse(event.data);
        handleCrisisEvent(data);
      };

      es.onerror = (error) => {
        console.error('SSE Error:', error);
        es.close();
      };
    } catch (error) {
      console.error('Error starting crisis:', error);
    }
  }, []);

  const handleCrisisEvent = (event) => {
    console.log('Crisis event:', event);

    switch (event.type) {
      case 'alert_detected':
        setState(CRISIS_STATES.ALERT_DETECTED);
        setAlert(event.data);
        break;

      case 'agent_reasoning':
        setState(CRISIS_STATES.AGENTS_REASONING);
        setAgents((prev) => {
          const existing = prev.find((a) => a.agent === event.data.agent);
          if (existing) {
            return prev.map((a) =>
              a.agent === event.data.agent ? event.data : a
            );
          }
          return [...prev, event.data];
        });
        break;

      case 'debate_start':
        setState(CRISIS_STATES.DEBATE);
        setDebate(event.data);
        break;

      case 'financial_update':
        setFinancialData(event.data);
        break;

      case 'debate_verdict':
        setDebate((prev) => ({ ...prev, verdict: event.data }));
        break;

      case 'hitl_prompt':
        setState(CRISIS_STATES.AWAITING_APPROVAL);
        setRecommendation(event.data);
        break;

      case 'crisis_resolved':
        setState(CRISIS_STATES.RESOLVED);
        break;

      case 'complete':
        if (eventSource) eventSource.close();
        break;

      default:
        console.warn('Unknown event type:', event.type);
    }
  };

  const approveDecision = useCallback(async () => {
    try {
      const response = await fetch('http://localhost:8000/api/decision/approve', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ id: 'demo_decision', action: 'approve' }),
      });

      if (response.ok) {
        setState(CRISIS_STATES.RESOLVED);
        setTimeout(() => resetCrisis(), 5000);
      }
    } catch (error) {
      console.error('Error approving decision:', error);
    }
  }, []);

  const resetCrisis = useCallback(async () => {
    try {
      await fetch('http://localhost:8000/api/demo/reset', { method: 'POST' });
      setState(CRISIS_STATES.NORMAL);
      setAlert(null);
      setAgents([]);
      setDebate(null);
      setFinancialData(null);
      setRecommendation(null);
      if (eventSource) {
        eventSource.close();
        setEventSource(null);
      }
    } catch (error) {
      console.error('Error resetting crisis:', error);
    }
  }, [eventSource]);

  const value = {
    state,
    alert,
    agents,
    debate,
    financialData,
    recommendation,
    startCrisis,
    approveDecision,
    resetCrisis,
    CRISIS_STATES,
  };

  return <CrisisContext.Provider value={value}>{children}</CrisisContext.Provider>;
};

export default CrisisContext;