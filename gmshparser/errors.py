from __future__ import annotations

from dataclasses import dataclass

__all__ = [
    "GmshError",
    "InvalidElementConnectivityError",
    "InvalidElementError",
    "InvalidMeshError",
    "InvalidNodeError",
    "InvalidSectionError",
    "ParseError",
    "ParsingContext",
    "UnexpectedEndOfFileError",
    "UnknownElementTypeError",
    "UnsupportedBinaryFormatError",
    "UnsupportedVersionError",
]


@dataclass(slots=True)
class ParsingContext:
    """Current source location while parsing an MSH stream."""

    filename: str | None = None
    line_number: int = 0
    section: str | None = None
    line: str | None = None

    def copy(self, **changes: object) -> ParsingContext:
        """Return an independent context snapshot with optional replacements."""
        values: dict[str, object] = {
            "filename": self.filename,
            "line_number": self.line_number,
            "section": self.section,
            "line": self.line,
        }
        values.update(changes)
        return ParsingContext(**values)  # type: ignore[arg-type]


class GmshError(Exception):
    """Base class for public gmshparser errors."""


class ParseError(GmshError, ValueError):
    """Base class for malformed or unsupported MSH input.

    ``ParseError`` remains a :class:`ValueError` for compatibility with code that
    caught parser failures before the structured error hierarchy was introduced.
    """

    def __init__(
        self,
        message: str,
        *,
        filename: str | None = None,
        line_number: int | None = None,
        section: str | None = None,
        line: str | None = None,
    ) -> None:
        self.message = message
        self.filename = filename
        self.line_number = line_number
        self.section = section
        self.line = line
        super().__init__(message)

    def __str__(self) -> str:
        location = self.filename
        if location is not None and self.line_number is not None:
            location = f"{location}:{self.line_number}"
        elif location is None and self.line_number is not None:
            location = f"line {self.line_number}"

        if self.section is not None:
            section = f"[{self.section}]"
            location = f"{location} {section}" if location else section

        return f"{location}: {self.message}" if location else self.message

    def with_context(self, context: ParsingContext) -> ParseError:
        """Return the same error type with missing source fields populated."""
        return type(self)(
            self.message,
            filename=self.filename or context.filename,
            line_number=(
                self.line_number
                if self.line_number is not None
                else context.line_number or None
            ),
            section=self.section or context.section,
            line=self.line if self.line is not None else context.line,
        )


class UnsupportedVersionError(ParseError):
    """Raised when an MSH version is not supported."""


class UnsupportedBinaryFormatError(ParseError):
    """Raised when a binary MSH stream is supplied to the ASCII parser."""


class UnexpectedEndOfFileError(ParseError):
    """Raised when an MSH section ends before its declared contents."""


class InvalidSectionError(ParseError):
    """Raised when a section header, record, or end marker is malformed."""


class InvalidNodeError(ParseError):
    """Raised when a node record or node block is malformed."""


class InvalidElementError(ParseError):
    """Raised when an element record or element block is malformed."""


class InvalidElementConnectivityError(InvalidElementError):
    """Raised when element connectivity has an invalid width."""


class UnknownElementTypeError(InvalidElementError):
    """Raised when topology metadata is required for an unknown element type."""


class InvalidMeshError(ParseError):
    """Raised when parsed sections cannot form a consistent modern mesh."""
