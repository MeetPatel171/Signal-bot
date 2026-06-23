.PHONY: run test setup-browser send-test-notification inspect lint clean

run:
	uv run python -m signal_bot

test:
	uv run pytest -v

setup-browser:
	uv run python scripts/setup_browser.py

send-test-notification:
	uv run python scripts/send_test_notification.py

inspect:
	uv run python scripts/inspect_positions.py

lint:
	uv run ruff check src tests scripts

clean:
	rm -rf .pytest_cache .ruff_cache
	find . -type d -name __pycache__ -exec rm -rf {} +
