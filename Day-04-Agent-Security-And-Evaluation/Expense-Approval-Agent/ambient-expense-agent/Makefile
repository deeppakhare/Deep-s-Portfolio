.PHONY: install run eval lint format playground

install:
	uv sync

run:
	uv run agents-cli run "Review travel expense of 150 USD"

eval:
	uv run agents-cli eval run

lint:
	uv run ruff check .
	uv run mypy .

format:
	uv run ruff format .

playground:
	adk web

ambient:
	uv run uvicorn expense_agent.fast_api_app:app --host 0.0.0.0 --port 8080

generate-traces:
	uv run python tests/eval/generate_traces.py

grade:
	uv run agents-cli eval run