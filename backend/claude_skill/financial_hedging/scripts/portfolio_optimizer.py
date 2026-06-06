"""Portfolio Optimizer — financial hedging skill tool.

Ported from Vector897/Globot. Greedy multi-instrument portfolio allocator
that picks the most cost-effective hedging instruments first, subject to
per-instrument capacity caps and an optional total budget.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Dict, List, Optional


@dataclass
class HedgeInstrument:
    """A single hedging instrument with cost, protection, and capacity."""

    name: str
    cost_per_unit: float
    protection_per_unit: float
    max_capacity: float


def optimize_hedge_portfolio(
    exposure: float,
    target_hedge_ratio: float,
    instruments: List[HedgeInstrument],
    budget_constraint: Optional[float] = None,
) -> Dict:
    """Greedy minimum-cost portfolio optimisation.

    Picks instruments in order of best cost-per-unit-protection ratio until
    either the target protection is reached, the per-instrument cap is hit,
    or (if provided) the budget is exhausted.
    """
    target_protection = exposure * target_hedge_ratio

    scored: List[tuple] = []
    for inst in instruments:
        if inst.protection_per_unit > 0:
            ratio = inst.cost_per_unit / inst.protection_per_unit
            scored.append((inst, ratio))
    scored.sort(key=lambda x: x[1])

    allocations: List[Dict] = []
    total_cost = 0.0
    total_protection = 0.0
    remaining_target = target_protection

    for inst, _ratio in scored:
        if remaining_target <= 0:
            break

        desired_units = min(
            remaining_target / inst.protection_per_unit,
            inst.max_capacity,
        )

        if budget_constraint is not None:
            if inst.cost_per_unit > 0:
                max_affordable = (budget_constraint - total_cost) / inst.cost_per_unit
                desired_units = min(desired_units, max(max_affordable, 0))

        if desired_units > 0:
            allocation_cost = desired_units * inst.cost_per_unit
            allocation_protection = desired_units * inst.protection_per_unit
            allocations.append(
                {
                    "instrument": inst.name,
                    "units": desired_units,
                    "cost": allocation_cost,
                    "protection": allocation_protection,
                    "percentage_of_target": (allocation_protection / target_protection) * 100
                    if target_protection
                    else 0.0,
                }
            )
            total_cost += allocation_cost
            total_protection += allocation_protection
            remaining_target -= allocation_protection

    achieved_ratio = total_protection / exposure if exposure > 0 else 0.0

    return {
        "target_hedge_ratio": target_hedge_ratio * 100,
        "achieved_hedge_ratio": achieved_ratio * 100,
        "total_cost": total_cost,
        "total_protection": total_protection,
        "cost_per_protection": total_cost / total_protection if total_protection > 0 else 0.0,
        "allocations": allocations,
        "optimization_efficiency": (achieved_ratio / target_hedge_ratio) * 100
        if target_hedge_ratio
        else 0.0,
    }


def create_fuel_hedging_portfolio(
    exposure_tons: float,
    current_price: float,
    target_ratio: float = 0.70,
    budget: Optional[float] = None,
) -> Dict:
    """Optimised fuel-hedging portfolio across futures, swaps, and options."""
    exposure_usd = exposure_tons * current_price

    instruments = [
        HedgeInstrument(
            name="Futures (3-month rolling)",
            cost_per_unit=current_price * 0.02,
            protection_per_unit=current_price * 1.0,
            max_capacity=exposure_tons * 0.50,
        ),
        HedgeInstrument(
            name="Swaps (6-month)",
            cost_per_unit=2.0,
            protection_per_unit=current_price * 1.0,
            max_capacity=exposure_tons * 0.30,
        ),
        HedgeInstrument(
            name="Put Options (protective)",
            cost_per_unit=current_price * 0.05,
            protection_per_unit=current_price * 0.90,
            max_capacity=exposure_tons * 0.25,
        ),
        HedgeInstrument(
            name="Collar Options (zero-cost)",
            cost_per_unit=current_price * 0.01,
            protection_per_unit=current_price * 0.85,
            max_capacity=exposure_tons * 0.20,
        ),
    ]

    return optimize_hedge_portfolio(
        exposure=exposure_usd,
        target_hedge_ratio=target_ratio,
        instruments=instruments,
        budget_constraint=budget,
    )


def create_currency_hedging_portfolio(
    exposure_foreign_currency: float,
    fx_rate: float,
    target_ratio: float = 0.70,
) -> Dict:
    """Optimised FX-hedging portfolio: forwards-heavy with protective puts."""
    exposure_usd = exposure_foreign_currency * fx_rate

    instruments = [
        HedgeInstrument(
            name="1-month Forward",
            cost_per_unit=0.0,
            protection_per_unit=fx_rate * 1.0,
            max_capacity=exposure_foreign_currency * 0.30,
        ),
        HedgeInstrument(
            name="3-month Forward",
            cost_per_unit=0.0,
            protection_per_unit=fx_rate * 0.995,
            max_capacity=exposure_foreign_currency * 0.30,
        ),
        HedgeInstrument(
            name="6-month Forward",
            cost_per_unit=0.0,
            protection_per_unit=fx_rate * 0.99,
            max_capacity=exposure_foreign_currency * 0.20,
        ),
        HedgeInstrument(
            name="FX Options (protective put)",
            cost_per_unit=fx_rate * 0.02,
            protection_per_unit=fx_rate * 0.95,
            max_capacity=exposure_foreign_currency * 0.20,
        ),
    ]

    return optimize_hedge_portfolio(
        exposure=exposure_usd,
        target_hedge_ratio=target_ratio,
        instruments=instruments,
    )
