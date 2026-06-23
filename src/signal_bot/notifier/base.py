"""Notifier protocol. See plan §4.4."""
from dataclasses import dataclass
from typing import Literal, Protocol


ResponseKind = Literal["approve", "reject", "skip", "timeout", "clarify"]


@dataclass
class Proposal:
    id: str
    text: str


@dataclass
class ClarificationOption:
    id: str
    label: str


@dataclass
class Response:
    kind: ResponseKind
    raw_text: str | None
    clarify_option_id: str | None = None


class Notifier(Protocol):
    async def send_proposal(self, proposal: Proposal, timeout_seconds: int) -> Response: ...
    async def send_alert(self, message: str) -> None: ...
    async def send_clarification(
        self, options: list[ClarificationOption], timeout_seconds: int
    ) -> Response: ...
