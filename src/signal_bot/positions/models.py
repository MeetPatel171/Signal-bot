"""Position-layer dataclasses. See plan §4.6."""
from dataclasses import dataclass
from datetime import datetime
from typing import Literal


@dataclass
class Position:
    id: str
    ticker: str
    direction: Literal["long", "short"]
    quantity: float
    entry_price: float
    entry_time: datetime
    current_stop: float | None
    current_target: float | None
    status: Literal["open", "closed", "stopped_out", "error"]
    source_message_id: str | None
    source_trader: str | None
    closed_at: datetime | None
    realized_pnl: float | None
    notes: str | None
