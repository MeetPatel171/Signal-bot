"""Shared SQLite connection + schema. See plan §4.6.1 and §4.9.

All tables live in a single DB file. WAL mode lets the reader, orchestrator,
and position manager run concurrently without lock contention.
"""
from __future__ import annotations

import sqlite3
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parent.parent.parent
DATA_DIR = PROJECT_ROOT / "data"
DB_PATH = DATA_DIR / "positions.db"

SCHEMA = """
CREATE TABLE IF NOT EXISTS positions (
    id TEXT PRIMARY KEY,
    ticker TEXT NOT NULL,
    direction TEXT NOT NULL,
    quantity REAL NOT NULL,
    entry_price REAL NOT NULL,
    entry_time DATETIME NOT NULL,
    current_stop REAL,
    current_target REAL,
    status TEXT NOT NULL,
    source_message_id TEXT,
    source_trader TEXT,
    closed_at DATETIME,
    realized_pnl REAL,
    notes TEXT
);

CREATE TABLE IF NOT EXISTS orders (
    id TEXT PRIMARY KEY,
    position_id TEXT NOT NULL,
    type TEXT NOT NULL,
    side TEXT NOT NULL,
    quantity REAL NOT NULL,
    price REAL,
    status TEXT NOT NULL,
    placed_at DATETIME NOT NULL,
    filled_at DATETIME,
    fill_price REAL,
    FOREIGN KEY (position_id) REFERENCES positions(id)
);

CREATE TABLE IF NOT EXISTS position_updates (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    position_id TEXT NOT NULL,
    timestamp DATETIME NOT NULL,
    update_type TEXT NOT NULL,
    details JSON NOT NULL,
    source TEXT NOT NULL,
    source_ref TEXT
);

CREATE TABLE IF NOT EXISTS reader_state (
    channel_id TEXT PRIMARY KEY,
    last_message_id TEXT NOT NULL,
    last_processed_at DATETIME NOT NULL
);
"""


def get_connection(db_path: Path | None = None) -> sqlite3.Connection:
    path = db_path or DB_PATH
    path.parent.mkdir(parents=True, exist_ok=True)
    conn = sqlite3.connect(path)
    conn.execute("PRAGMA journal_mode=WAL")
    conn.execute("PRAGMA foreign_keys=ON")
    conn.row_factory = sqlite3.Row
    return conn


def init_db(db_path: Path | None = None) -> None:
    with get_connection(db_path) as conn:
        conn.executescript(SCHEMA)
