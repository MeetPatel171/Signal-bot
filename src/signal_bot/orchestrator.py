"""Orchestrator — coordinates reader, parsers, filter, notifier, executor, position manager.

See plan §4.9. Phase 0: init DB, write startup audit event, log ready.
"""
from __future__ import annotations

import logging

from signal_bot import db
from signal_bot.audit import log as audit

logger = logging.getLogger(__name__)


def main() -> None:
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s %(levelname)s %(name)s: %(message)s",
    )

    logger.info("signal-bot starting — Phase 0 scaffold")

    db.init_db()
    logger.info("db initialized at %s", db.DB_PATH)

    audit.write_event(
        event_type="startup",
        payload={"phase": "0", "mode": "stub"},
        correlation_id=audit.new_correlation_id(),
    )
    logger.info("orchestrator ready; no loops wired yet")
