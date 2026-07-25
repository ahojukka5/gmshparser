from __future__ import annotations

from typing import TextIO

from .abstract_parser import AbstractParser
from .elements_parser import ElementsParser
from .elements_parser_v1 import ElementsParserV1
from .elements_parser_v2 import ElementsParserV2
from .entities_parser import EntitiesParser
from .errors import InvalidSectionError
from .mesh import Mesh
from .mesh_format_parser import MeshFormatParser
from .nodes_parser import NodesParser
from .nodes_parser_v1 import NodesParserV1
from .nodes_parser_v2 import NodesParserV2
from .parsing import SourceTextIO, contextualize_error
from .periodic_parser import PeriodicParser
from .physical_names_parser import PhysicalNamesParser

# Default parsers for MSH 4.x format
DEFAULT_PARSERS_V4 = [
    MeshFormatParser,
    PhysicalNamesParser,
    EntitiesParser,
    NodesParser,
    ElementsParser,
    PeriodicParser,
]

# Default parsers for MSH 2.x format
DEFAULT_PARSERS_V2 = [
    MeshFormatParser,
    PhysicalNamesParser,
    NodesParserV2,
    ElementsParserV2,
    PeriodicParser,
]

# Parsers for MSH 1.0 format (no MeshFormatParser needed)
DEFAULT_PARSERS_V1 = [
    NodesParserV1,
    ElementsParserV1,
]


class MainParser(AbstractParser):
    """Route MSH sections to version-specific parsers with source context."""

    def __init__(self, parsers=None):
        self.parsers = parsers
        self.version_detected = False

    def parse(self, mesh: Mesh, io: TextIO) -> None:
        """Parse an MSH stream and populate *mesh*.

        All section failures are exposed as structured ``ParseError`` subclasses
        carrying the source name, current section, line number, and line text.
        """
        self.version_detected = False
        filename = mesh.get_name() or str(getattr(io, "name", "<stream>"))
        source = io if isinstance(io, SourceTextIO) else SourceTextIO(io, filename)
        context = source.context

        for raw_line in source:
            line = raw_line.strip()
            if not line:
                continue

            if line == "$NOD" and not self.version_detected:
                mesh.set_version(1.0)
                self.version_detected = True
                if self.parsers is None:
                    self.parsers = DEFAULT_PARSERS_V1
                self._parse_section(NodesParserV1, mesh, source, line)
                continue

            if line == "$MeshFormat" and not self.version_detected:
                self._parse_section(MeshFormatParser, mesh, source, line)
                self.version_detected = True
                if self.parsers is None:
                    self.parsers = self._get_parsers_for_version(mesh)
                continue

            if self.parsers:
                for parser in self.parsers:
                    if parser.get_section_name() == line:
                        self._parse_section(parser, mesh, source, line)
                        break

        context.section = None
        if not self.version_detected:
            raise InvalidSectionError(
                "Could not detect a supported MSH format",
                filename=context.filename,
                line_number=context.line_number or None,
                line=context.line,
            )

    @staticmethod
    def _parse_section(
        parser: type[AbstractParser],
        mesh: Mesh,
        source: SourceTextIO,
        section: str,
    ) -> None:
        context = source.context
        context.section = section
        try:
            parser.parse(mesh, source)
        except Exception as error:
            contextual = contextualize_error(error, context)
            if contextual is error:
                raise
            raise contextual from error
        finally:
            context.section = None

    def _get_parsers_for_version(self, mesh: Mesh) -> list[type[AbstractParser]]:
        """Return the parser set for the detected major MSH version."""
        version = mesh.get_version()
        if version is None:
            raise InvalidSectionError(
                "Cannot determine parsers because the version was not detected"
            )

        major = mesh.get_version_major()
        if major == 1:
            return DEFAULT_PARSERS_V1
        if major == 2:
            return DEFAULT_PARSERS_V2
        if major == 4:
            return DEFAULT_PARSERS_V4
        raise InvalidSectionError(f"Unsupported MSH format version: {version}")
