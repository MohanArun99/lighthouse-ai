"""Financial hedging skill scripts.

Pure-Python, stdlib-only calculators ported from
Vector897/Globot ``backend/claude_skill/financial_hedging/scripts``.
Exposed as deterministic tools for the LLM-driven Financial Hedge Strategist.
"""

from .risk_calculator import (
    calculate_var,
    calculate_optimal_hedge_ratio,
    calculate_hedge_cost_benefit,
    calculate_portfolio_risk,
)
from .portfolio_optimizer import (
    HedgeInstrument,
    optimize_hedge_portfolio,
    create_fuel_hedging_portfolio,
    create_currency_hedging_portfolio,
)

__all__ = [
    "calculate_var",
    "calculate_optimal_hedge_ratio",
    "calculate_hedge_cost_benefit",
    "calculate_portfolio_risk",
    "HedgeInstrument",
    "optimize_hedge_portfolio",
    "create_fuel_hedging_portfolio",
    "create_currency_hedging_portfolio",
]
