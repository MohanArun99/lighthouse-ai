import React from 'react';
import { Box, Card, CardContent, Typography, Chip, LinearProgress, Paper } from '@mui/material';
import ArrowDownwardIcon from '@mui/icons-material/ArrowDownward';
import EmojiEventsIcon from '@mui/icons-material/EmojiEvents';

const DebatePanel = ({ redTeam, blueTeam, verdict }) => {
  const winner = verdict?.winner;

  const TeamCard = ({ team, color, isWinner }) => (
    <Card
      sx={{
        flex: 1,
        background: `linear-gradient(135deg, rgba(${color}, 0.1) 0%, rgba(13, 27, 42, 0.95) 100%)`,
        backdropFilter: 'blur(10px)',
        border: `2px solid ${isWinner ? `rgba(${color}, 0.8)` : `rgba(${color}, 0.3)`}`,
        boxShadow: isWinner ? `0 0 30px rgba(${color}, 0.4)` : '0 8px 32px rgba(0, 0, 0, 0.3)',
        transition: 'all 0.5s ease',
        transform: isWinner ? 'scale(1.02)' : 'scale(1)',
        animation: 'slideIn 0.5s ease',
        '@keyframes slideIn': {
          from: { opacity: 0, transform: 'translateX(-20px)' },
          to: { opacity: 1, transform: 'translateX(0)' },
        },
      }}
    >
      <CardContent>
        <Box display="flex" alignItems="center" gap={1} mb={2}>
          <Typography variant="h4" sx={{ fontSize: 28 }}>
            {team.icon}
          </Typography>
          <Typography
            variant="h6"
            sx={{
              color: `rgb(${color})`,
              fontWeight: 700,
              textTransform: 'uppercase',
              letterSpacing: 1,
            }}
          >
            {team.agent}
          </Typography>
          {isWinner && (
            <EmojiEventsIcon
              sx={{
                color: 'gold',
                fontSize: 28,
                ml: 'auto',
                animation: 'bounce 1s infinite',
                '@keyframes bounce': {
                  '0%, 100%': { transform: 'translateY(0)' },
                  '50%': { transform: 'translateY(-10px)' },
                },
              }}
            />
          )}
        </Box>

        <Typography
          variant="body1"
          sx={{
            color: 'text.primary',
            mb: 2,
            lineHeight: 1.6,
            fontFamily: 'system-ui',
          }}
        >
          {team.argument}
        </Typography>

        <Box sx={{ mb: 2 }}>
          <Typography variant="caption" sx={{ color: 'text.disabled', mb: 0.5 }}>
            Confidence Level
          </Typography>
          <Box display="flex" alignItems="center" gap={1}>
            <LinearProgress
              variant="determinate"
              value={team.confidence}
              sx={{
                flex: 1,
                height: 8,
                borderRadius: 4,
                bgcolor: 'rgba(255, 255, 255, 0.1)',
                '& .MuiLinearProgress-bar': {
                  bgcolor: `rgb(${color})`,
                  transition: 'transform 1s ease',
                },
              }}
            />
            <Typography
              variant="body2"
              sx={{ color: `rgb(${color})`, fontWeight: 700, minWidth: 40 }}
            >
              {team.confidence}%
            </Typography>
          </Box>
        </Box>

        <Box>
          <Typography variant="caption" sx={{ color: 'text.disabled', mb: 1, display: 'block' }}>
            Supporting Data:
          </Typography>
          {team.supporting_data?.map((data, index) => (
            <Chip
              key={index}
              label={data}
              size="small"
              sx={{
                mb: 0.5,
                mr: 0.5,
                bgcolor: `rgba(${color}, 0.2)`,
                color: `rgb(${color})`,
                fontSize: 11,
                height: 24,
              }}
            />
          ))}
        </Box>
      </CardContent>
    </Card>
  );

  return (
    <Box>
      <Typography
        variant="h5"
        sx={{
          color: 'primary.light',
          fontWeight: 700,
          mb: 3,
          textAlign: 'center',
          textTransform: 'uppercase',
          letterSpacing: 2,
        }}
      >
        ⚔️ Adversarial Debate
      </Typography>

      <Box display="flex" gap={2} mb={3}>
        <TeamCard
          team={redTeam}
          color="220, 38, 38"
          isWinner={winner === 'red_team'}
        />
        <TeamCard
          team={blueTeam}
          color="59, 130, 246"
          isWinner={winner === 'blue_team'}
        />
      </Box>

      {verdict && (
        <Paper
          sx={{
            p: 3,
            bgcolor: 'rgba(34, 197, 94, 0.1)',
            border: '2px solid rgba(34, 197, 94, 0.3)',
            borderRadius: 2,
            animation: 'fadeIn 0.5s ease',
            '@keyframes fadeIn': {
              from: { opacity: 0, transform: 'translateY(20px)' },
              to: { opacity: 1, transform: 'translateY(0)' },
            },
          }}
        >
          <Box display="flex" alignItems="center" gap={2} mb={2}>
            <ArrowDownwardIcon sx={{ color: 'success.main', fontSize: 28 }} />
            <Typography variant="h6" sx={{ color: 'success.main', fontWeight: 700 }}>
              VERDICT
            </Typography>
          </Box>
          <Typography variant="body1" sx={{ color: 'text.primary', mb: 2 }}>
            {verdict.reason}
          </Typography>
          <Box
            sx={{
              p: 2,
              bgcolor: 'rgba(34, 197, 94, 0.2)',
              borderRadius: 1,
              borderLeft: '4px solid rgb(34, 197, 94)',
            }}
          >
            <Typography variant="body2" sx={{ color: 'success.light', fontWeight: 600 }}>
              Final Recommendation: {verdict.final_recommendation?.action} via{' '}
              {verdict.final_recommendation?.route}
            </Typography>
            <Typography variant="caption" sx={{ color: 'text.secondary' }}>
              Estimated Savings: ${(verdict.final_recommendation?.estimated_savings || 0).toLocaleString()}
            </Typography>
          </Box>
        </Paper>
      )}
    </Box>
  );
};

export default DebatePanel;