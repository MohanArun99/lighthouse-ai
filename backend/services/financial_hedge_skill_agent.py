"""Live Financial Hedge Strategist agent powered by Databricks Model Serving.

Wires the financial-hedging Claude skill (``backend/claude_skill/financial_hedging``)
to a single Claude model served via Databricks (default
``databricks-claude-3-7-sonnet``) using the OpenAI-compatible chat completions
API with tool calling.

Design notes
------------
* This agent is *only* invoked when ``LIVE_AGENTS`` env var contains the
  literal string ``Financial Hedge Strategist``.
* On *any* failure (missing creds, timeout, network error, malformed JSON,
  schema-validation error) the caller in ``main.py`` falls back to the
  scripted card from ``crisis_sequence.py`` — so the demo never breaks.
* Tools exposed to the LLM are pure-stdlib calculators ported from Vector897/
  Globot (see ``backend/claude_skill/financial_hedging/scripts``).
"""

from __future__ import annotations

import json
import logging
import os
import time
from typing import Any, Dict, List, Optional

from pydantic import BaseModel, Field, ValidationError, field_validator

from claude_skill.financial_hedging import load_skill_md
from claude_skill.financial_hedging.scripts import (
    calculate_hedge_cost_benefit,
    calculate_optimal_hedge_ratio,
    calculate_portfolio_risk,
    calculate_var,
    create_currency_hedging_portfolio,
    create_fuel_hedging_portfolio,
)

logger = logging.getLogger(__name__)


DEFAULT_MODEL = "databricks-claude-3-7-sonnet"
DEFAULT_MAX_TOOL_ROUNDS = 4


# ---------------------------------------------------------------------------
# Output schema (must match AgentThinkingCard props in the frontend)
# ---------------------------------------------------------------------------


class AgentStep(BaseModel):
    step: int
    description: str
    status: str = "complete"
    duration: float = 0.0


class AgentCard(BaseModel):
    agent: str
    icon: str = "💰"
    status: str = "complete"
    steps: List[AgentStep]
    sources: List[str]
    conclusion: str

    @field_validator("steps")
    @classmethod
    def _three_steps(cls, v: List[AgentStep]) -> List[AgentStep]:
        if not 1 <= len(v) <= 5:
            raise ValueError("agent must produce 1–5 steps")
        return v


# ---------------------------------------------------------------------------
# Tool registry (executed locally; the LLM only orchestrates)
# ---------------------------------------------------------------------------


_TOOL_HANDLERS: Dict[str, Any] = {
    "calculate_var": calculate_var,
    "calculate_optimal_hedge_ratio": calculate_optimal_hedge_ratio,
    "calculate_hedge_cost_benefit": calculate_hedge_cost_benefit,
    "calculate_portfolio_risk": calculate_portfolio_risk,
    "create_fuel_hedging_portfolio": create_fuel_hedging_portfolio,
    "create_currency_hedging_portfolio": create_currency_hedging_portfolio,
}


def _tool_specs() -> List[Dict[str, Any]]:
    """OpenAI-compatible tool specifications for the LLM."""
    return [
        {
            "type": "function",
            "function": {
                "name": "calculate_var",
                "description": (
                    "Parametric Value-at-Risk for an exposure. Returns var_usd, "
                    "var_pct, and a textual interpretation."
                ),
                "parameters": {
                    "type": "object",
                    "properties": {
                        "exposure": {"type": "number", "description": "Total exposure in USD."},
                        "volatility": {
                            "type": "number",
                            "description": "Annualised volatility, e.g. 0.20 for 20%.",
                        },
                        "confidence": {
                            "type": "number",
                            "enum": [0.90, 0.95, 0.99],
                            "default": 0.95,
                        },
                        "horizon_days": {"type": "integer", "default": 180},
                    },
                    "required": ["exposure", "volatility"],
                },
            },
        },
        {
            "type": "function",
            "function": {
                "name": "calculate_optimal_hedge_ratio",
                "description": "Minimum-variance optimal hedge ratio h* = ρ · (σ_spot/σ_futures).",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "correlation": {"type": "number"},
                        "spot_volatility": {"type": "number"},
                        "futures_volatility": {"type": "number"},
                    },
                    "required": ["correlation", "spot_volatility", "futures_volatility"],
                },
            },
        },
        {
            "type": "function",
            "function": {
                "name": "calculate_hedge_cost_benefit",
                "description": "ROI of a candidate hedge — protection vs premium.",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "exposure": {"type": "number"},
                        "hedge_cost": {"type": "number"},
                        "volatility": {"type": "number"},
                        "hedge_ratio": {"type": "number", "default": 0.70},
                    },
                    "required": ["exposure", "hedge_cost", "volatility"],
                },
            },
        },
        {
            "type": "function",
            "function": {
                "name": "create_fuel_hedging_portfolio",
                "description": (
                    "Optimised fuel-hedging portfolio across futures, swaps, put "
                    "options, and collars."
                ),
                "parameters": {
                    "type": "object",
                    "properties": {
                        "exposure_tons": {"type": "number"},
                        "current_price": {"type": "number"},
                        "target_ratio": {"type": "number", "default": 0.70},
                        "budget": {"type": "number"},
                    },
                    "required": ["exposure_tons", "current_price"],
                },
            },
        },
        {
            "type": "function",
            "function": {
                "name": "create_currency_hedging_portfolio",
                "description": "Forwards-heavy FX-hedging portfolio.",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "exposure_foreign_currency": {"type": "number"},
                        "fx_rate": {"type": "number"},
                        "target_ratio": {"type": "number", "default": 0.70},
                    },
                    "required": ["exposure_foreign_currency", "fx_rate"],
                },
            },
        },
    ]


def _execute_tool(name: str, arguments: Dict[str, Any]) -> Dict[str, Any]:
    """Run a tool locally and return its JSON-serialisable result."""
    handler = _TOOL_HANDLERS.get(name)
    if handler is None:
        return {"error": f"unknown tool: {name}"}
    try:
        result = handler(**arguments)
        json.dumps(result)
        return result
    except Exception as exc:
        logger.warning("tool %s failed: %s", name, exc)
        return {"error": str(exc)}


# ---------------------------------------------------------------------------
# LLM client (Databricks Model Serving, OpenAI-compatible)
# ---------------------------------------------------------------------------


def _build_client() -> Any:
    """Construct an OpenAI-compatible client pointed at Databricks Model Serving.

    Raises ``RuntimeError`` if creds or the SDK are missing — caller catches.
    """
    try:
        from openai import OpenAI
    except ImportError as exc:
        raise RuntimeError(
            "openai package is not installed; live agent disabled"
        ) from exc

    host = os.environ.get("DATABRICKS_HOST")
    token = os.environ.get("DATABRICKS_TOKEN")
    if not host or not token:
        raise RuntimeError(
            "DATABRICKS_HOST / DATABRICKS_TOKEN not set; live agent disabled"
        )

    base_url = host.rstrip("/") + "/serving-endpoints"
    return OpenAI(api_key=token, base_url=base_url)


def _user_prompt(crisis_context: Dict[str, Any], scripted_card: Dict[str, Any]) -> str:
    """Pack the crisis context the orchestrator already gathered."""
    return (
        "Crisis context (JSON):\n"
        + json.dumps(crisis_context, indent=2)
        + "\n\nScripted reference card (your live output should mirror its shape "
        "but with computed numbers):\n"
        + json.dumps(scripted_card, indent=2)
        + "\n\nPlan: call the relevant tools, then emit the final JSON object "
        "as instructed in the SKILL.md system prompt. Output ONLY the JSON object."
    )


def _extract_json(text: str) -> Dict[str, Any]:
    """Lenient JSON extractor — strips code fences if the model added them."""
    text = text.strip()
    if text.startswith("```"):
        first = text.find("\n")
        last = text.rfind("```")
        if first != -1 and last != -1:
            text = text[first + 1 : last].strip()
    return json.loads(text)


# ---------------------------------------------------------------------------
# Public entry point
# ---------------------------------------------------------------------------


async def generate_financial_hedge_card(
    crisis_context: Dict[str, Any],
    scripted_card: Dict[str, Any],
    *,
    model: Optional[str] = None,
    max_tool_rounds: int = DEFAULT_MAX_TOOL_ROUNDS,
) -> Dict[str, Any]:
    """Run one Claude invocation with the financial-hedging skill.

    Returns a dict matching ``AgentCard``. Raises on any failure so the caller
    can fall back to the scripted card.
    """
    import asyncio

    model = model or os.environ.get("LIVE_MODEL", DEFAULT_MODEL)
    client = _build_client()
    skill_md = load_skill_md()
    tools = _tool_specs()

    messages: List[Dict[str, Any]] = [
        {"role": "system", "content": skill_md},
        {"role": "user", "content": _user_prompt(crisis_context, scripted_card)},
    ]

    started = time.monotonic()

    for round_idx in range(max_tool_rounds):
        # The OpenAI SDK is sync; run it in a worker thread so we don't block
        # the FastAPI event loop / SSE generator.
        response = await asyncio.to_thread(
            client.chat.completions.create,
            model=model,
            messages=messages,
            tools=tools,
            tool_choice="auto",
            temperature=0.3,
            max_tokens=900,
        )

        choice = response.choices[0]
        message = choice.message

        tool_calls = getattr(message, "tool_calls", None) or []

        # Append the assistant turn so the conversation history is valid.
        assistant_turn: Dict[str, Any] = {
            "role": "assistant",
            "content": message.content or "",
        }
        if tool_calls:
            assistant_turn["tool_calls"] = [
                {
                    "id": tc.id,
                    "type": "function",
                    "function": {
                        "name": tc.function.name,
                        "arguments": tc.function.arguments,
                    },
                }
                for tc in tool_calls
            ]
        messages.append(assistant_turn)

        if not tool_calls:
            text = message.content or ""
            try:
                payload = _extract_json(text)
            except json.JSONDecodeError as exc:
                raise RuntimeError(
                    f"agent returned non-JSON content: {text[:200]!r}"
                ) from exc
            card = AgentCard(**payload)
            elapsed = time.monotonic() - started
            logger.info(
                "live financial_hedge agent ok in %.2fs (rounds=%d)",
                elapsed,
                round_idx + 1,
            )
            return card.model_dump()

        for tc in tool_calls:
            try:
                args = json.loads(tc.function.arguments or "{}")
            except json.JSONDecodeError:
                args = {}
            tool_result = _execute_tool(tc.function.name, args)
            messages.append(
                {
                    "role": "tool",
                    "tool_call_id": tc.id,
                    "content": json.dumps(tool_result),
                }
            )

    raise RuntimeError(
        f"agent exceeded max_tool_rounds={max_tool_rounds} without final answer"
    )


__all__ = ["generate_financial_hedge_card", "AgentCard"]
