"""Append-only JSONL audit log. See plan §4.7.

Every meaningful event in the system writes through here. Daily-rotated files
at logs/audit-YYYY-MM-DD.jsonl, one JSON object per line.
"""
from __future__ import annotations

import json
from datetime import datetime
from pathlib import Path
from threading import Lock
from typing import Any
from uuid import uuid4

PROJECT_ROOT = Path(__file__).resolve().parent.parent.parent.parent
LOGS_DIR = PROJECT_ROOT / "logs"

_write_lock = Lock()


def _log_path(now: datetime | None = None) -> Path:
    now = now or datetime.now()
    return LOGS_DIR / f"audit-{now.strftime('%Y-%m-%d')}.jsonl"


def new_correlation_id() -> str:
    return uuid4().hex[:12]


def write_event(
    event_type: str,
    payload: dict[str, Any],
    correlation_id: str | None = None,
    logs_dir: Path | None = None,
) -> None:
    logs_dir = logs_dir or LOGS_DIR
    logs_dir.mkdir(parents=True, exist_ok=True)
    record = {
        "timestamp": datetime.now().isoformat(timespec="microseconds"),
        "event_type": event_type,
        "correlation_id": correlation_id,
        "payload": payload,
    }
    line = json.dumps(record, default=str)
    path = logs_dir / f"audit-{datetime.now().strftime('%Y-%m-%d')}.jsonl"
    with _write_lock, path.open("a") as f:
        f.write(line + "\n")
