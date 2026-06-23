"""Parser-output dataclasses. See plan §4.2."""
from dataclasses import dataclass
from typing import Literal


@dataclass
class Signal:
    is_trade: bool
    ticker: str | None
    direction: Literal["buy", "sell", "short", "cover"] | None
    order_type: Literal["market", "limit"] | None
    limit_price: float | None
    entry_zone: tuple[float, float] | None
    stop_loss: float | None
    target: float | None
    suggested_size_hint: str | None
    confidence: Literal["high", "medium", "low"]
    is_hypothetical: bool
    is_correction: bool
    has_chart: bool
    chart_observations: str | None
    reasoning: str
    source_quote: str


@dataclass
class PositionUpdate:
    is_update: bool
    position_id: str | None
    update_type: Literal["stop_change", "scale_in", "scale_out", "exit", "note"] | None
    new_stop: float | None
    scale_quantity_pct: float | None
    exit_price: float | None
    confidence: Literal["high", "medium", "low"]
    ambiguous_match: bool
    candidate_position_ids: list[str]
    reasoning: str
    source_quote: str
