"""Risk Calculator — financial hedging skill tool.

Ported from Vector897/Globot ``backend/claude_skill/financial_hedging/scripts/risk_calculator.py``.
Pure-stdlib math (parametric VaR, optimal hedge ratio, cost/benefit, portfolio
risk). Used as deterministic LLM tools by the Financial Hedge Strategist agent.
"""

from __future__ import annotations

import math
from typing import Dict, Optional


_Z_SCORES = {0.90: 1.282, 0.95: 1.645, 0.99: 2.326}


def calculate_var(
    exposure: float,
    volatility: float,
    confidence: float = 0.95,
    horizon_days: int = 180,
) -> Dict:
    """Parametric Value-at-Risk.

    Args:
        exposure: Total exposure in USD.
        volatility: Annualised volatility (e.g. ``0.20`` for 20%).
        confidence: Confidence level (``0.90``, ``0.95``, or ``0.99``).
        horizon_days: Horizon in calendar days.
    """
    horizon_volatility = volatility * math.sqrt(horizon_days / 252)
    z_score = _Z_SCORES.get(confidence, 1.645)

    var_usd = exposure * z_score * horizon_volatility
    var_pct = (var_usd / exposure) * 100 if exposure else 0.0

    return {
        "exposure": exposure,
        "volatility_annual": volatility * 100,
        "horizon_days": horizon_days,
        "confidence_level": confidence * 100,
        "var_usd": var_usd,
        "var_pct": var_pct,
        "interpretation": _interpret_var(var_pct),
    }


def calculate_optimal_hedge_ratio(
    correlation: float,
    spot_volatility: float,
    futures_volatility: float,
) -> Dict:
    """Minimum-variance optimal hedge ratio: ``h* = ρ · (σ_spot / σ_futures)``."""
    if futures_volatility == 0:
        raise ValueError("futures_volatility must be non-zero")

    optimal_ratio = correlation * (spot_volatility / futures_volatility)
    variance_reduction = correlation ** 2

    if correlation > 0.85:
        effectiveness = "High"
    elif correlation > 0.70:
        effectiveness = "Medium"
    else:
        effectiveness = "Low"

    return {
        "optimal_hedge_ratio": optimal_ratio,
        "recommended_pct": min(optimal_ratio * 100, 85.0),
        "variance_reduction_pct": variance_reduction * 100,
        "hedge_effectiveness": effectiveness,
    }


def calculate_hedge_cost_benefit(
    exposure: float,
    hedge_cost: float,
    volatility: float,
    hedge_ratio: float = 0.70,
) -> Dict:
    """Cost/benefit analysis of a candidate hedge."""
    expected_loss_unhedged = exposure * volatility
    expected_protection = expected_loss_unhedged * hedge_ratio

    roi = expected_protection / hedge_cost if hedge_cost > 0 else float("inf")
    breakeven_move_pct = (hedge_cost / exposure) * 100 if exposure else 0.0

    if roi > 5:
        recommendation = "Hedge"
    elif roi > 2:
        recommendation = "Consider"
    else:
        recommendation = "Not Recommended"

    return {
        "hedge_cost_usd": hedge_cost,
        "hedge_cost_pct": (hedge_cost / exposure) * 100 if exposure else 0.0,
        "expected_protection_usd": expected_protection,
        "roi_ratio": roi,
        "breakeven_move_pct": breakeven_move_pct,
        "recommendation": recommendation,
    }


def calculate_portfolio_risk(
    fuel_exposure: float,
    currency_exposure: float,
    freight_exposure: float,
    fuel_vol: float,
    currency_vol: float,
    freight_vol: float,
    correlations: Optional[Dict[str, float]] = None,
) -> Dict:
    """Portfolio variance with cross-asset correlations."""
    if correlations is None:
        correlations = {
            "fuel_currency": 0.0,
            "fuel_freight": 0.3,
            "currency_freight": 0.0,
        }

    total_exposure = fuel_exposure + currency_exposure + freight_exposure
    if total_exposure == 0:
        raise ValueError("total exposure must be non-zero")

    w_fuel = fuel_exposure / total_exposure
    w_currency = currency_exposure / total_exposure
    w_freight = freight_exposure / total_exposure

    var_fuel = (w_fuel * fuel_vol) ** 2
    var_currency = (w_currency * currency_vol) ** 2
    var_freight = (w_freight * freight_vol) ** 2

    cov_fuel_currency = (
        2 * w_fuel * w_currency * correlations["fuel_currency"] * fuel_vol * currency_vol
    )
    cov_fuel_freight = (
        2 * w_fuel * w_freight * correlations["fuel_freight"] * fuel_vol * freight_vol
    )
    cov_currency_freight = (
        2
        * w_currency
        * w_freight
        * correlations["currency_freight"]
        * currency_vol
        * freight_vol
    )

    portfolio_variance = (
        var_fuel
        + var_currency
        + var_freight
        + cov_fuel_currency
        + cov_fuel_freight
        + cov_currency_freight
    )
    portfolio_volatility = math.sqrt(portfolio_variance)

    simple_sum_volatility = (
        w_fuel * fuel_vol + w_currency * currency_vol + w_freight * freight_vol
    )
    diversification_benefit = simple_sum_volatility - portfolio_volatility

    return {
        "total_exposure_usd": total_exposure,
        "portfolio_volatility": portfolio_volatility * 100,
        "individual_risks": {
            "fuel": {
                "exposure": fuel_exposure,
                "contribution": (var_fuel / portfolio_variance) * 100
                if portfolio_variance
                else 0.0,
            },
            "currency": {
                "exposure": currency_exposure,
                "contribution": (var_currency / portfolio_variance) * 100
                if portfolio_variance
                else 0.0,
            },
            "freight": {
                "exposure": freight_exposure,
                "contribution": (var_freight / portfolio_variance) * 100
                if portfolio_variance
                else 0.0,
            },
        },
        "diversification_benefit_pct": diversification_benefit * 100,
        "correlations": correlations,
    }


def _interpret_var(var_pct: float) -> str:
    if var_pct > 20:
        return "Critical risk - immediate hedging required"
    if var_pct > 15:
        return "High risk - hedging strongly recommended"
    if var_pct > 10:
        return "Moderate risk - consider hedging"
    return "Low risk - selective hedging"
