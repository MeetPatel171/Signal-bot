"""Executor protocol. See plan §4.5."""
from dataclasses import dataclass
from typing import Literal, Protocol


@dataclass
class EntryProposal:
    ticker: str
    quantity: float
    order_type: Literal["market", "limit"]
    limit_price: float | None
    stop_price: float | None


@dataclass
class ExecutionResult:
    success: bool
    order_id: str | None
    fill_price: float | None
    error: str | None


@dataclass
class BrokerPosition:
    ticker: str
    quantity: float
    avg_entry_price: float


@dataclass
class Quote:
    ticker: str
    last: float
    bid: float | None
    ask: float | None


class Executor(Protocol):
    async def place_entry(self, proposal: EntryProposal) -> ExecutionResult: ...
    async def place_stop(
        self, position_id: str, stop_price: float, qty: float
    ) -> ExecutionResult: ...
    async def modify_stop(self, order_id: str, new_stop: float) -> ExecutionResult: ...
    async def cancel_order(self, order_id: str) -> ExecutionResult: ...
    async def close_position(
        self, position_id: str, qty_pct: float, order_type: str
    ) -> ExecutionResult: ...
    async def get_positions(self) -> list[BrokerPosition]: ...
    async def get_quote(self, ticker: str) -> Quote: ...
