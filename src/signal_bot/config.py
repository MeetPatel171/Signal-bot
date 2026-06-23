"""Typed config loaders for YAML rules + .env. See plan §5.

Pydantic validates at load time so malformed config fails fast rather than
deep in the filter / position-manager call paths.
"""
from __future__ import annotations

import os
from pathlib import Path
from typing import Literal

import yaml
from dotenv import load_dotenv
from pydantic import BaseModel, Field

PROJECT_ROOT = Path(__file__).resolve().parent.parent.parent
CONFIG_DIR = PROJECT_ROOT / "config"


# === rules.yaml: entries section ===

class RiskRules(BaseModel):
    max_position_dollars: float
    max_position_pct_account: float
    max_concurrent_positions: int
    max_daily_trades: int
    max_daily_loss_dollars: float
    cooldown_seconds_after_trade: int


class UniverseRules(BaseModel):
    allowed_tickers: list[str] | None
    blocked_tickers: list[str]
    min_price: float
    max_price: float
    require_listed_exchange: bool


class SignalRules(BaseModel):
    min_confidence: Literal["high", "medium", "low"]
    reject_hypotheticals: bool
    reject_corrections: bool


class TimeWindowRules(BaseModel):
    trading_only: bool
    blackout_minutes_around_open: int
    blackout_minutes_around_close: int
    timezone: str


class SizeHintMultipliers(BaseModel):
    starter: float
    small: float
    normal: float
    full: float


class ExecutionRules(BaseModel):
    default_order_type: Literal["market", "limit"]
    limit_offset_pct: float
    default_size_dollars: float
    size_hint_multipliers: SizeHintMultipliers
    auto_place_stop: bool
    default_stop_pct: float


class EntryRules(BaseModel):
    risk: RiskRules
    universe: UniverseRules
    signal: SignalRules
    time_windows: TimeWindowRules
    execution: ExecutionRules


# === rules.yaml: position_management section ===

class ManualUpdateRules(BaseModel):
    require_hitl: bool
    min_confidence: Literal["high", "medium", "low"]
    reject_ambiguous: bool


class BreakevenRule(BaseModel):
    enabled: bool
    trigger_gain_pct: float
    require_hitl: bool


class TrailingStopRule(BaseModel):
    enabled: bool
    activate_gain_pct: float
    trail_distance_pct: float
    require_hitl: bool


class EodFlattenRule(BaseModel):
    enabled: bool
    time: str  # "HH:MM" in configured timezone
    action: Literal["market_close"]
    require_hitl: bool


class TimeStopRule(BaseModel):
    enabled: bool
    max_hold_minutes: int


class AutoRules(BaseModel):
    breakeven_move: BreakevenRule
    trailing_stop: TrailingStopRule
    eod_flatten: EodFlattenRule
    time_stop: TimeStopRule


class ScalingRules(BaseModel):
    max_adds_per_position: int
    max_total_size_multiplier: float


class PositionManagementRules(BaseModel):
    manual_updates: ManualUpdateRules
    auto_rules: AutoRules
    scaling: ScalingRules


class Rules(BaseModel):
    entries: EntryRules
    position_management: PositionManagementRules


# === channels.yaml / traders.yaml ===

class Channel(BaseModel):
    name: str
    url: str


class _ChannelsFile(BaseModel):
    channels: list[Channel] = Field(default_factory=list)


class Trader(BaseModel):
    username: str
    weight: float = 1.0


class _TradersFile(BaseModel):
    traders: list[Trader] = Field(default_factory=list)


# === .env ===

class EnvConfig(BaseModel):
    anthropic_api_key: str
    notifier: Literal["imessage", "twilio"]
    user_phone_number: str
    twilio_account_sid: str | None = None
    twilio_auth_token: str | None = None
    twilio_from_number: str | None = None
    executor_mode: Literal["paper", "live"]
    log_level: str = "INFO"
    timezone: str = "America/New_York"


# === Loaders ===

def _read_yaml(path: Path) -> dict:
    with path.open("r") as f:
        return yaml.safe_load(f) or {}


def load_rules(path: Path | None = None) -> Rules:
    return Rules.model_validate(_read_yaml(path or CONFIG_DIR / "rules.yaml"))


def load_channels(path: Path | None = None) -> list[Channel]:
    return _ChannelsFile.model_validate(_read_yaml(path or CONFIG_DIR / "channels.yaml")).channels


def load_traders(path: Path | None = None) -> list[Trader]:
    return _TradersFile.model_validate(_read_yaml(path or CONFIG_DIR / "traders.yaml")).traders


def load_env(env_path: Path | None = None) -> EnvConfig:
    load_dotenv(env_path or PROJECT_ROOT / ".env")
    return EnvConfig(
        anthropic_api_key=os.environ["ANTHROPIC_API_KEY"],
        notifier=os.environ.get("NOTIFIER", "imessage"),  # type: ignore[arg-type]
        user_phone_number=os.environ["USER_PHONE_NUMBER"],
        twilio_account_sid=os.environ.get("TWILIO_ACCOUNT_SID") or None,
        twilio_auth_token=os.environ.get("TWILIO_AUTH_TOKEN") or None,
        twilio_from_number=os.environ.get("TWILIO_FROM_NUMBER") or None,
        executor_mode=os.environ.get("EXECUTOR_MODE", "paper"),  # type: ignore[arg-type]
        log_level=os.environ.get("LOG_LEVEL", "INFO"),
        timezone=os.environ.get("TIMEZONE", "America/New_York"),
    )


class Config(BaseModel):
    env: EnvConfig
    rules: Rules
    channels: list[Channel]
    traders: list[Trader]


def load_config() -> Config:
    return Config(
        env=load_env(),
        rules=load_rules(),
        channels=load_channels(),
        traders=load_traders(),
    )
