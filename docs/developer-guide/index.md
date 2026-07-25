# Developer Guide

This guide covers repository development, parser architecture, validation, testing, documentation, and release preparation.

## Start here

- [Architecture](architecture.md) explains the shared parsing pipeline and the two public data models.
- [Contributing](contributing.md) defines the development environment and pull-request expectations.
- [Writing Parsers](writing-parsers.md) describes how to add or extend MSH section support.
- [Parser Internals](parser-internals.md) lists the parser classes and version registries.
- [Testing](testing.md) documents the test layout and required checks.
- [Performance Benchmarks](benchmarks.md) explains the reproducible benchmark suite.
- [Test Results](test-results.md) points to CI and coverage as the authoritative status.

## Local validation

```bash
uv sync
uv run ruff format --check gmshparser tests examples benchmarks
uv run ruff check gmshparser tests examples benchmarks
uv run mypy gmshparser
uv run mypy --strict tests/typing/public_api.py
uv run pytest
uv sync --group docs
uv run mkdocs build --strict
uv build --no-sources
```

A change to parser behavior should normally include a focused fixture, tests for both `gmshparser.parse()` and `gmshparser.read()`, and corresponding user/API documentation.
