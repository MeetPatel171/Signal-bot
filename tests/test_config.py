"""rules.yaml must validate against the Pydantic models we ship."""
from signal_bot.config import load_channels, load_rules, load_traders


def test_rules_yaml_validates():
    rules = load_rules()
    assert rules.entries.risk.max_position_dollars == 500
    assert rules.entries.signal.min_confidence == "medium"
    assert rules.position_management.auto_rules.breakeven_move.trigger_gain_pct == 1.0
    assert rules.position_management.auto_rules.eod_flatten.time == "15:55"


def test_channels_yaml_loads_empty():
    assert load_channels() == []


def test_traders_yaml_loads_empty():
    assert load_traders() == []
