"""Phase 0 smoke test: package imports cleanly."""


def test_package_imports():
    import signal_bot  # noqa: F401
    from signal_bot import orchestrator  # noqa: F401
    from signal_bot.executor.base import Executor  # noqa: F401
    from signal_bot.notifier.base import Notifier  # noqa: F401
    from signal_bot.parser.models import PositionUpdate, Signal  # noqa: F401
    from signal_bot.reader.models import Message  # noqa: F401
