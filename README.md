# Signal-bot

Local Python app that monitors a Discord trading community, extracts trade signals (text + images + embeds) with an LLM, asks the user for approval via iMessage, and executes via the Robinhood Agentic Trading MCP. Human-in-the-loop by default.

Full design and phasing in `signal-bot-plan.md` (kept separately on Desktop).

## Quickstart

```bash
uv sync
cp .env.example .env   # fill in ANTHROPIC_API_KEY and USER_PHONE_NUMBER
make run               # Phase 0 stub: logs startup and exits
```

## Status

Phase 0 — scaffold. Components are stubbed; no live behavior yet.
