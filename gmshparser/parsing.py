from __future__ import annotations

from collections.abc import Iterator
from typing import Any, TextIO

from .errors import (
    InvalidElementError,
    InvalidNodeError,
    InvalidSectionError,
    ParseError,
    ParsingContext,
    UnexpectedEndOfFileError,
)

__all__ = [
    "SourceTextIO",
    "contextualize_error",
    "expect_end_marker",
    "get_parsing_context",
    "read_required_line",
]


class SourceTextIO:
    """Text stream proxy that records the current source line."""

    __slots__ = ("_stream", "context")

    def __init__(self, stream: TextIO, filename: str | None = None) -> None:
        self._stream = stream
        self.context = ParsingContext(filename=filename)

    def readline(self, size: int = -1) -> str:
        line = self._stream.readline(size)
        if line != "":
            self.context.line_number += 1
            self.context.line = line.rstrip("\r\n")
        return line

    def __iter__(self) -> Iterator[str]:
        return self

    def __next__(self) -> str:
        line = self.readline()
        if line == "":
            raise StopIteration
        return line

    def __getattr__(self, name: str) -> Any:
        return getattr(self._stream, name)


def get_parsing_context(io: TextIO) -> ParsingContext | None:
    """Return parser context when *io* is a tracked source stream."""
    context = getattr(io, "context", None)
    return context if isinstance(context, ParsingContext) else None


def read_required_line(io: TextIO, description: str) -> str:
    """Read one line or raise a contextual unexpected-EOF error."""
    line = io.readline()
    if line != "":
        return line

    context = get_parsing_context(io)
    if context is None:
        raise UnexpectedEndOfFileError(
            f"Unexpected end of file while reading {description}"
        )

    raise UnexpectedEndOfFileError(
        f"Unexpected end of file while reading {description}",
        filename=context.filename,
        line_number=context.line_number + 1,
        section=context.section,
        line=None,
    )


def expect_end_marker(io: TextIO, marker: str) -> None:
    """Consume and validate a section end marker."""
    line = read_required_line(io, marker)
    actual = line.strip()
    if actual != marker:
        raise InvalidSectionError(f"Expected {marker}, got {actual!r}")


def contextualize_error(
    error: Exception,
    context: ParsingContext,
) -> ParseError:
    """Convert a parser failure into the appropriate public error type."""
    if isinstance(error, ParseError):
        if (
            error.filename is not None
            or error.line_number is not None
            or error.section is not None
        ):
            return error
        return error.with_context(context)

    if context.section in {"$Nodes", "$NOD"}:
        error_type: type[ParseError] = InvalidNodeError
    elif context.section in {"$Elements", "$ELM"}:
        error_type = InvalidElementError
    else:
        error_type = InvalidSectionError

    message = str(error) or type(error).__name__
    return error_type(
        message,
        filename=context.filename,
        line_number=context.line_number or None,
        section=context.section,
        line=context.line,
    )
