import React, { useState, useEffect } from 'react';
import { Card, CardContent, Typography, Box, Divider, Chip } from '@mui/material';
import TrendingUpIcon from '@mui/icons-material/TrendingUp';
import TrendingDownIcon from '@mui/icons-material/TrendingDown';
import CheckCircleIcon from '@mui/icons-material/CheckCircle';

const AnimatedNumber = ({ value, duration = 2000, prefix = '', suffix = '', color = 'inherit' }) => {
  const [displayValue, setDisplayValue] = useState(0);

  useEffect(() => {
    let startTime;
    const animate = (timestamp) => {
      if (!startTime) startTime = timestamp;
      const progress = Math.min((timestamp - startTime) / duration, 1);
      
      // Easing function for smooth animation
      const easeOutQuad = (t) => t * (2 - t);
      const currentValue = Math.floor(value * easeOutQuad(progress));
      
      setDisplayValue(currentValue);
      
      if (progress < 1) {
        requestAnimationFrame(animate);
      }
    };
    
    requestAnimationFrame(animate);
  }, [value, duration]);

  return (
    <Typography
      variant="h4"
      sx={{
        color,
        fontWeight: 700,
        fontFamily: 'monospace',
        letterSpacing: 1,
      }}
    >
      {prefix}{displayValue.toLocaleString()}{suffix}
    </Typography>
  );
};

const FinancialImpactWidget = ({ data }) => {
  if (!data) return null;

  const {
    original_cost,
    fuel_premium,
    insurance_savings,
    net_savings,
    hedge_recommendation,
  } = data;

  const fuelPercentage = ((fuel_premium / original_cost) * 100).toFixed(1);
  const insurancePercentage = ((Math.abs(insurance_savings) / original_cost) * 100).toFixed(1);

  return (
    <Card
      sx={{
        background: 'linear-gradient(135deg, rgba(13, 27, 42, 0.95) 0%, rgba(30, 58, 138, 0.9) 100%)',
        backdropFilter: 'blur(10px)',
        border: '2px solid rgba(251, 191, 36, 0.3)',
        boxShadow: '0 12px 48px rgba(251, 191, 36, 0.2)',
        animation: 'slideIn 0.5s ease',
        '@keyframes slideIn': {
          from: { opacity: 0, transform: 'translateY(20px)' },
          to: { opacity: 1, transform: 'translateY(0)' },
        },
      }}
    >
      <CardContent sx={{ p: 3 }}>
        <Box display="flex" alignItems="center" gap={1} mb={3}>
          <Typography variant="h3" sx={{ fontSize: 28 }}>
            💰
          </Typography>
          <Typography
            variant="h5"
            sx={{
              color: 'warning.light',
              fontWeight: 700,
              textTransform: 'uppercase',
              letterSpacing: 1,
            }}
          >
            Financial Impact
          </Typography>
        </Box>

        {/* Original Route Cost */}
        <Box mb={2}>
          <Typography variant="caption" sx={{ color: 'text.disabled', mb: 0.5 }}>
            Original Route Cost
          </Typography>
          <AnimatedNumber value={original_cost} prefix="$" color="text.primary" />
        </Box>

        <Divider sx={{ my: 2, bgcolor: 'rgba(255, 255, 255, 0.1)' }} />

        {/* Fuel Premium */}
        <Box display="flex" justifyContent="space-between" alignItems="center" mb={2}>
          <Box>
            <Typography variant="body2" sx={{ color: 'text.secondary', mb: 0.5 }}>
              Reroute Fuel Premium
            </Typography>
            <AnimatedNumber value={fuel_premium} prefix="+$" color="error.main" />
          </Box>
          <Box display="flex" alignItems="center" gap={0.5}>
            <TrendingUpIcon sx={{ color: 'error.main', fontSize: 20 }} />
            <Typography variant="h6" sx={{ color: 'error.main', fontWeight: 700 }}>
              {fuelPercentage}%
            </Typography>
          </Box>
        </Box>

        {/* Insurance Savings */}
        <Box display="flex" justifyContent="space-between" alignItems="center" mb={2}>
          <Box>
            <Typography variant="body2" sx={{ color: 'text.secondary', mb: 0.5 }}>
              Insurance Savings
            </Typography>
            <AnimatedNumber value={Math.abs(insurance_savings)} prefix="-$" color="success.main" />
          </Box>
          <Box display="flex" alignItems="center" gap={0.5}>
            <TrendingDownIcon sx={{ color: 'success.main', fontSize: 20 }} />
            <Typography variant="h6" sx={{ color: 'success.main', fontWeight: 700 }}>
              {insurancePercentage}%
            </Typography>
          </Box>
        </Box>

        <Divider sx={{ my: 2, bgcolor: 'rgba(255, 255, 255, 0.2)' }} />

        {/* Net Savings */}
        <Box
          sx={{
            p: 2,
            bgcolor: 'rgba(34, 197, 94, 0.15)',
            borderRadius: 2,
            border: '2px solid rgba(34, 197, 94, 0.3)',
            mb: 3,
          }}
        >
          <Box display="flex" justifyContent="space-between" alignItems="center">
            <Box>
              <Typography variant="body2" sx={{ color: 'success.light', mb: 0.5 }}>
                NET SAVINGS
              </Typography>
              <AnimatedNumber value={net_savings} prefix="$" color="success.main" duration={2500} />
            </Box>
            <CheckCircleIcon
              sx={{
                color: 'success.main',
                fontSize: 48,
                animation: 'pulse 2s infinite',
                '@keyframes pulse': {
                  '0%, 100%': { transform: 'scale(1)', opacity: 1 },
                  '50%': { transform: 'scale(1.1)', opacity: 0.8 },
                },
              }}
            />
          </Box>
        </Box>

        {/* Hedge Recommendation */}
        {hedge_recommendation && (
          <Box
            sx={{
              p: 2,
              bgcolor: 'rgba(59, 130, 246, 0.1)',
              borderRadius: 2,
              border: '1px solid rgba(59, 130, 246, 0.3)',
            }}
          >
            <Typography variant="caption" sx={{ color: 'text.disabled', mb: 1, display: 'block' }}>
              Hedge Recommendation:
            </Typography>
            <Box display="flex" alignItems="center" gap={1} mb={1}>
              <Chip
                label={hedge_recommendation.action}
                size="small"
                sx={{
                  bgcolor: 'primary.main',
                  color: 'white',
                  fontWeight: 700,
                }}
              />
              <Typography variant="body2" sx={{ color: 'primary.light', fontWeight: 600 }}>
                {hedge_recommendation.instrument}
              </Typography>
            </Box>
            <Typography variant="caption" sx={{ color: 'text.secondary' }}>
              {hedge_recommendation.contracts} contracts @ ${hedge_recommendation.entry_price}/bbl → target ${hedge_recommendation.target_price}
            </Typography>
            <Typography variant="caption" sx={{ color: 'success.light', display: 'block', mt: 0.5 }}>
              Expected Gain: ${hedge_recommendation.expected_gain?.toLocaleString()}
            </Typography>
          </Box>
        )}
      </CardContent>
    </Card>
  );
};

export default FinancialImpactWidget;