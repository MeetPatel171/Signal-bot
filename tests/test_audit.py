"""Audit log writes parseable JSONL records to the expected path."""
import json
from datetime import datetime

from signal_bot.audit import log as audit


def test_write_event_creates_jsonl_record(tmp_path):
    cid = audit.new_correlation_id()
    audit.write_event(
        event_type="test_event",
        payload={"foo": "bar", "n": 1, "when": datetime.now()},
        correlation_id=cid,
        logs_dir=tmp_path,
    )

    log_file = tmp_path / f"audit-{datetime.now().strftime('%Y-%m-%d')}.jsonl"
    assert log_file.exists()
    record = json.loads(log_file.read_text().strip())
    assert record["event_type"] == "test_event"
    assert record["correlation_id"] == cid
    assert record["payload"]["foo"] == "bar"
    assert "timestamp" in record


def test_write_event_appends(tmp_path):
    for i in range(3):
        audit.write_event("evt", {"i": i}, logs_dir=tmp_path)
    log_file = tmp_path / f"audit-{datetime.now().strftime('%Y-%m-%d')}.jsonl"
    lines = log_file.read_text().strip().splitlines()
    assert len(lines) == 3


def test_correlation_id_is_short_hex():
    cid = audit.new_correlation_id()
    assert len(cid) == 12
    int(cid, 16)  # parses as hex
