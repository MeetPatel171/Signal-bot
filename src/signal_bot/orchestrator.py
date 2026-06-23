"""Orchestrator — coordinates reader, parsers, filter, notifier, executor, position manager.

See plan §4.9. Phase 0: prove the import graph boots and logging works.
"""
import logging

log = logging.getLogger(__name__)


def main() -> None:
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s %(levelname)s %(name)s: %(message)s",
    )
    log.info("signal-bot starting — Phase 0 scaffold")
    log.info("orchestrator stub OK; no loops wired yet")
