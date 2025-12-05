install:
	uv sync

verify:
	uv run pyright
	uv run pytest --durations=5
