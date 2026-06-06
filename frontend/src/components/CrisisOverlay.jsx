import React from 'react';
import {
  Box,
  Paper,
  Typography,
  Button,
  Alert,
  AlertTitle,
  Fade,
  Slide,
  LinearProgress,
} from '@mui/material';
import { useCrisis } from '../context/CrisisContext';
import AgentThinkingCard from './AgentThinkingCard';
import DebatePanel from './DebatePanel';
import FinancialImpactWidget from './FinancialImpactWidget';
import WarningAmberIcon from '@mui/icons-material/WarningAmber';
import CheckCircleIcon from '@mui/icons-material/CheckCircle';

const CrisisOverlay = () => {
  const {
    state,
    alert,
    agents,
    debate,
    financialData,
    recommendation,
    approveDecision,
    resetCrisis,
    CRISIS_STATES,
  } = useCrisis();

  if (state === CRISIS_STATES.NORMAL) return null;

  const isResolved = state === CRISIS_STATES.RESOLVED;

  return (
    <Fade in timeout={500}>
      <Box
        sx={{
          position: 'fixed',
          top: 0,
          left: 0,
          right: 0,
          bottom: 0,
          bgcolor: 'rgba(0, 0, 0, 0.85)',
          backdropFilter: 'blur(8px)',
          zIndex: 9999,
          overflow: 'auto',
          p: 3,
        }}
      >
        <Box maxWidth={1400} mx="auto">
          {/* Alert Banner */}
          {alert && state === CRISIS_STATES.ALERT_DETECTED && (
            <Slide direction="down" in mountOnEnter unmountOnExit>
              <Alert
                severity="error"
                icon={<WarningAmberIcon sx={{ fontSize: 32 }} />}
                sx={{
                  mb: 3,
                  bgcolor: 'rgba(220, 38, 38, 0.2)',
                  border: '2px solid rgb(220, 38, 38)',
                  animation: 'pulse 2s infinite',
                  '@keyframes pulse': {
                    '0%, 100%': { boxShadow: '0 0 20px rgba(220, 38, 38, 0.5)' },
                    '50%': { boxShadow: '0 0 40px rgba(220, 38, 38, 0.8)' },
                  },
                }}
              >
                <AlertTitle sx={{ fontSize: 20, fontWeight: 700 }}>
                  {alert.title}
                </AlertTitle>
                <Typography variant="body1">{alert.message}</Typography>
                <Box display="flex" gap={2} mt={1}>
                  <Typography variant="caption">
                    Source: {alert.source} | Confidence: {alert.confidence}%
                  </Typography>
                  <Typography variant="caption" sx={{ color: 'error.light', fontWeight: 700 }}>
                    Risk Level: {alert.risk_level}
                  </Typography>
                </Box>
              </Alert>
            </Slide>
          )}

          {/* Agents Reasoning */}
          {state === CRISIS_STATES.AGENTS_REASONING && agents.length > 0 && (
            <Box mb={3}>
              <Typography
                variant="h4"
                sx={{
                  color: 'primary.light',
                  fontWeight: 700,
                  mb: 2,
                  textTransform: 'uppercase',
                  letterSpacing: 2,
                }}
              >
                🤖 AI Agents Analyzing Crisis
              </Typography>
              <LinearProgress
                sx={{
                  mb: 3,
                  height: 4,
                  bgcolor: 'rgba(66, 153, 225, 0.2)',
                  '& .MuiLinearProgress-bar': {
                    bgcolor: 'primary.main',
                  },
                }}
              />
              {agents.map((agent, index) => (
                <AgentThinkingCard key={index} {...agent} />
              ))}
            </Box>
          )}

          {/* Financial Widget */}
          {financialData && (
            <Box mb={3}>
              <FinancialImpactWidget data={financialData} />
            </Box>
          )}

          {/* Debate Panel */}
          {debate && state === CRISIS_STATES.DEBATE && (
            <Box mb={3}>
              <DebatePanel
                redTeam={debate.red_team}
                blueTeam={debate.blue_team}
                verdict={debate.verdict}
              />
            </Box>
          )}

          {/* Human-in-the-Loop Approval */}
          {recommendation && state === CRISIS_STATES.AWAITING_APPROVAL && (
            <Paper
              sx={{
                p: 4,
                bgcolor: 'rgba(13, 27, 42, 0.95)',
                border: '3px solid rgba(251, 191, 36, 0.6)',
                boxShadow: '0 0 60px rgba(251, 191, 36, 0.4)',
                animation: 'glow 2s infinite',
                '@keyframes glow': {
                  '0%, 100%': { borderColor: 'rgba(251, 191, 36, 0.6)' },
                  '50%': { borderColor: 'rgba(251, 191, 36, 1)' },
                },
              }}
            >
              <Typography
                variant="h4"
                sx={{
                  color: 'warning.light',
                  fontWeight: 700,
                  mb: 2,
                  textAlign: 'center',
                }}
              >
                {recommendation.title}
              </Typography>
              <Typography
                variant="h6"
                sx={{ color: 'text.primary', mb: 3, textAlign: 'center' }}
              >
                {recommendation.message}
              </Typography>

              <Box
                sx={{
                  p: 3,
                  bgcolor: 'rgba(66, 153, 225, 0.1)',
                  borderRadius: 2,
                  mb: 3,
                }}
              >
                <Typography variant="h6" sx={{ color: 'primary.light', mb: 2 }}>
                  Recommendation Summary:
                </Typography>
                <Box display="grid" gridTemplateColumns="1fr 1fr" gap={2}>
                  <Box>
                    <Typography variant="caption" sx={{ color: 'text.disabled' }}>
                      Action
                    </Typography>
                    <Typography variant="body1" sx={{ color: 'text.primary', fontWeight: 600 }}>
                      {recommendation.recommendation.action}
                    </Typography>
                  </Box>
                  <Box>
                    <Typography variant="caption" sx={{ color: 'text.disabled' }}>
                      Confidence
                    </Typography>
                    <Typography variant="body1" sx={{ color: 'success.main', fontWeight: 600 }}>
                      {recommendation.recommendation.confidence}%
                    </Typography>
                  </Box>
                  <Box>
                    <Typography variant="caption" sx={{ color: 'text.disabled' }}>
                      Financial Impact
                    </Typography>
                    <Typography variant="body1" sx={{ color: 'success.main', fontWeight: 600 }}>
                      {recommendation.recommendation.financial_impact}
                    </Typography>
                  </Box>
                  <Box>
                    <Typography variant="caption" sx={{ color: 'text.disabled' }}>
                      Risk Reduction
                    </Typography>
                    <Typography variant="body1" sx={{ color: 'success.main', fontWeight: 600 }}>
                      {recommendation.recommendation.risk_reduction}
                    </Typography>
                  </Box>
                </Box>
              </Box>

              <Box display="flex" gap={2} justifyContent="center">
                {recommendation.options.map((option) => (
                  <Button
                    key={option.id}
                    variant="contained"
                    size="large"
                    onClick={() => option.id === 'approve' && approveDecision()}
                    sx={{
                      px: 4,
                      py: 1.5,
                      fontSize: 16,
                      fontWeight: 700,
                      bgcolor:
                        option.style === 'primary'
                          ? 'success.main'
                          : option.style === 'danger'
                          ? 'error.main'
                          : 'grey.700',
                      '&:hover': {
                        bgcolor:
                          option.style === 'primary'
                            ? 'success.dark'
                            : option.style === 'danger'
                            ? 'error.dark'
                            : 'grey.800',
                        transform: 'scale(1.05)',
                      },
                      transition: 'all 0.3s ease',
                      animation: option.style === 'primary' ? 'pulse 2s infinite' : 'none',
                    }}
                  >
                    {option.label}
                  </Button>
                ))}
              </Box>
            </Paper>
          )}

          {/* Resolution */}
          {isResolved && (
            <Paper
              sx={{
                p: 4,
                bgcolor: 'rgba(34, 197, 94, 0.2)',
                border: '3px solid rgb(34, 197, 94)',
                boxShadow: '0 0 60px rgba(34, 197, 94, 0.5)',
                textAlign: 'center',
                animation: 'sweepIn 1s ease',
                '@keyframes sweepIn': {
                  from: { opacity: 0, transform: 'scale(0.8)' },
                  to: { opacity: 1, transform: 'scale(1)' },
                },
              }}
            >
              <CheckCircleIcon
                sx={{
                  fontSize: 80,
                  color: 'success.main',
                  mb: 2,
                  animation: 'bounce 1s infinite',
                }}
              />
              <Typography variant="h3" sx={{ color: 'success.main', fontWeight: 700, mb: 2 }}>
                🎉 Crisis Contained
              </Typography>
              <Typography variant="h6" sx={{ color: 'text.primary', mb: 3 }}>
                All ships successfully rerouted. Financial hedges executed.
              </Typography>
              <Button
                variant="contained"
                size="large"
                onClick={resetCrisis}
                sx={{
                  px: 4,
                  py: 1.5,
                  fontSize: 16,
                  fontWeight: 700,
                  bgcolor: 'primary.main',
                  '&:hover': { bgcolor: 'primary.dark' },
                }}
              >
                Return to Dashboard
              </Button>
            </Paper>
          )}
        </Box>
      </Box>
    </Fade>
  );
};

export default CrisisOverlay;