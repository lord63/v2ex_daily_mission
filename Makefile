test:
	@uv run pytest tests/;

create:
	@uv build;

upload:
	@uv publish;
