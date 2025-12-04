verify:
	uv run pyright
	uv run pytest --durations=5
	make vulture
