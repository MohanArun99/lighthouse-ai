import React, { useEffect } from 'react';
import {
  Box,
  Container,
  Typography,
  Button,
  Grid,
  Card,
  CardContent,
  Chip,
} from '@mui/material';
import { useCrisis } from '../context/CrisisContext';
import CrisisOverlay from '../components/CrisisOverlay';
import DirectionsBoatIcon from '@mui/icons-material/DirectionsBoat';
import SecurityIcon from '@mui/icons-material/Security';
import TrendingUpIcon from '@mui/icons-material/TrendingUp';

const Dashboard = () => {
  const { state, startCrisis, CRISIS_STATES } = useCrisis();

  const isNormal = state === CRISIS_STATES.NORMAL;

  return (
    <Box
      sx={{
        minHeight: '100vh',
        bgcolor: 'rgb(13, 27, 42)',
        color: 'white',
        position: 'relative',
      }}
    >
      {/* Header */}
      <Box
        sx={{
          bgcolor: 'rgba(30, 58, 138, 0.3)',
          backdropFilter: 'blur(10px)',
          borderBottom: '1px solid rgba(66, 153, 225, 0.3)',
          py: 2,
        }}
      >
        <Container maxWidth="xl">
          <Box display="flex" justifyContent="space-between" alignItems="center">
            <Box display="flex" alignItems="center" gap={2}>
              <Typography variant="h3" sx={{ fontSize: 32, fontWeight: 700 }}>
                🌐
              </Typography>
              <Box>
                <Typography variant="h4" sx={{ fontWeight: 700, color: 'primary.light' }}>
                  Lighthouse AI
                </Typography>
                <Typography variant="caption" sx={{ color: 'text.disabled' }}>
                  Crisis Management & Risk Intelligence Platform
                </Typography>
              </Box>
            </Box>
            <Chip
              label={isNormal ? 'NORMAL OPERATIONS' : 'CRISIS MODE'}
              sx={{
                bgcolor: isNormal ? 'success.main' : 'error.main',
                color: 'white',
                fontWeight: 700,
                px: 2,
                fontSize: 14,
              }}
            />
          </Box>
        </Container>
      </Box>

      {/* Main Content */}
      <Container maxWidth="xl" sx={{ py: 4 }}>
        {/* Stats Cards */}
        <Grid container spacing={3} mb={4}>
          <Grid item xs={12} md={4}>
            <Card
              sx={{
                bgcolor: 'rgba(30, 58, 138, 0.2)',
                backdropFilter: 'blur(10px)',
                border: '1px solid rgba(66, 153, 225, 0.3)',
              }}
            >
              <CardContent>
                <Box display="flex" alignItems="center" gap={2}>
                  <DirectionsBoatIcon sx={{ fontSize: 40, color: 'primary.main' }} />
                  <Box>
                    <Typography variant="h3" sx={{ fontWeight: 700 }}>
                      3
                    </Typography>
                    <Typography variant="caption" sx={{ color: 'text.disabled' }}>
                      Ships Tracked
                    </Typography>
                  </Box>
                </Box>
              </CardContent>
            </Card>
          </Grid>
          <Grid item xs={12} md={4}>
            <Card
              sx={{
                bgcolor: 'rgba(30, 58, 138, 0.2)',
                backdropFilter: 'blur(10px)',
                border: '1px solid rgba(66, 153, 225, 0.3)',
              }}
            >
              <CardContent>
                <Box display="flex" alignItems="center" gap={2}>
                  <SecurityIcon sx={{ fontSize: 40, color: 'success.main' }} />
                  <Box>
                    <Typography variant="h3" sx={{ fontWeight: 700, color: 'success.main' }}>
                      35
                    </Typography>
                    <Typography variant="caption" sx={{ color: 'text.disabled' }}>
                      Risk Level (Low)
                    </Typography>
                  </Box>
                </Box>
              </CardContent>
            </Card>
          </Grid>
          <Grid item xs={12} md={4}>
            <Card
              sx={{
                bgcolor: 'rgba(30, 58, 138, 0.2)',
                backdropFilter: 'blur(10px)',
                border: '1px solid rgba(66, 153, 225, 0.3)',
              }}
            >
              <CardContent>
                <Box display="flex" alignItems="center" gap={2}>
                  <TrendingUpIcon sx={{ fontSize: 40, color: 'primary.main' }} />
                  <Box>
                    <Typography variant="h3" sx={{ fontWeight: 700 }}>
                      5
                    </Typography>
                    <Typography variant="caption" sx={{ color: 'text.disabled' }}>
                      AI Agents Active
                    </Typography>
                  </Box>
                </Box>
              </CardContent>
            </Card>
          </Grid>
        </Grid>

        {/* Demo Trigger */}
        <Box
          sx={{
            textAlign: 'center',
            py: 8,
            bgcolor: 'rgba(30, 58, 138, 0.1)',
            borderRadius: 2,
            border: '1px solid rgba(66, 153, 225, 0.2)',
          }}
        >
          <Typography variant="h4" sx={{ mb: 2, fontWeight: 600 }}>
            System Ready
          </Typography>
          <Typography variant="body1" sx={{ color: 'text.secondary', mb: 4, maxWidth: 600, mx: 'auto' }}>
            All systems operational. Click below to simulate a geopolitical crisis scenario
            and watch Lighthouse AI's multi-agent system respond in real-time.
          </Typography>
          <Button
            variant="contained"
            size="large"
            onClick={startCrisis}
            disabled={!isNormal}
            sx={{
              px: 6,
              py: 2,
              fontSize: 18,
              fontWeight: 700,
              bgcolor: 'error.main',
              '&:hover': {
                bgcolor: 'error.dark',
                transform: 'scale(1.05)',
              },
              '&:disabled': {
                bgcolor: 'grey.700',
              },
              transition: 'all 0.3s ease',
            }}
          >
            {isNormal ? '🚨 Start Crisis Scenario' : 'Crisis In Progress...'}
          </Button>
        </Box>

        {/* Footer Info */}
        <Box sx={{ mt: 6, textAlign: 'center' }}>
          <Typography variant="caption" sx={{ color: 'text.disabled' }}>
            Lighthouse AI v2.0 | Powered by Gemini 3.0 | 5-Agent Crisis Response System
          </Typography>
        </Box>
      </Container>

      {/* Crisis Overlay */}
      <CrisisOverlay />
    </Box>
  );
};

export default Dashboard;