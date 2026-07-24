from typing import TextIO

from .abstract_parser import AbstractParser
from .elements_parser import ElementsParser
from .elements_parser_v1 import ElementsParserV1
from .elements_parser_v2 import ElementsParserV2
from .entities_parser import EntitiesParser
from .mesh import Mesh
from .mesh_format_parser import MeshFormatParser
from .nodes_parser import NodesParser
from .nodes_parser_v1 import NodesParserV1
from .nodes_parser_v2 import NodesParserV2
from .physical_names_parser import PhysicalNamesParser

# Default parsers for MSH 4.x format
DEFAULT_PARSERS_V4 = [
    MeshFormatParser,
    PhysicalNamesParser,
    EntitiesParser,
    NodesParser,
    ElementsParser,
]

# Default parsers for MSH 2.x format
DEFAULT_PARSERS_V2 = [
    MeshFormatParser,
    PhysicalNamesParser,
    NodesParserV2,
    ElementsParserV2,
]

# Parsers for MSH 1.0 format (no MeshFormatParser needed)
DEFAULT_PARSERS_V1 = [
    NodesParserV1,
    ElementsParserV1,
]


class MainParser(AbstractParser):
    """The main parser class, using other parsers.

    This parser automatically detects the MSH format version and selects
    the appropriate parsers for that version.
    """

    def __init__(self, parsers=None):
        """Initialize the main parser.

        Parameters
        ----------
        parsers : list, optional
            List of parser classes to use. If None, parsers will be selected
            automatically based on the detected version.
        """
        self.parsers = parsers
        self.version_detected = False

    def parse(self, mesh: Mesh, io: TextIO) -> None:
        """Parse the mesh file.

        The parser first reads the MeshFormat section to detect the version,
        then selects the appropriate parsers for that version.

        For MSH 1.0 files (which don't have $MeshFormat), version is detected
        from the $NOD section name.

        Parameters
        ----------
        mesh : Mesh
            Mesh object to populate
        io : TextIO
            Input stream to read from

        Raises
        ------
        ValueError
            If the version is not supported or if parsing fails
        """
        for line in io:
            line = line.strip()

            if line == "$NOD" and not self.version_detected:
                mesh.set_version(1.0)
                self.version_detected = True

                if self.parsers is None:
                    self.parsers = DEFAULT_PARSERS_V1

                try:
                    NodesParserV1.parse(mesh, io)
                except Exception:
                    print(f"Unable to parse section {line} from mesh!")
                    raise
                continue

            if line == "$MeshFormat" and not self.version_detected:
                try:
                    MeshFormatParser.parse(mesh, io)
                    self.version_detected = True

                    if self.parsers is None:
                        self.parsers = self._get_parsers_for_version(mesh)

                except Exception:
                    print(f"Unable to parse section {line} from mesh!")
                    raise
                continue

            if self.parsers:
                for parser in self.parsers:
                    if parser.get_section_name() == line:
                        try:
                            parser.parse(mesh, io)
                        except Exception:
                            print(f"Unable to parse section {line} from mesh!")
                            raise
                        break

    def _get_parsers_for_version(self, mesh: Mesh) -> list[type[AbstractParser]]:
        """Get the appropriate parsers for the detected mesh version.

        Parameters
        ----------
        mesh : Mesh
            Mesh with version information

        Returns
        -------
        List[Type[AbstractParser]]
            List of parser classes to use

        Raises
        ------
        ValueError
            If version information is not available
        """
        version = mesh.get_version()
        if version is None:
            raise ValueError("Cannot determine parsers: version not detected")

        major = mesh.get_version_major()

        if major == 1:
            return DEFAULT_PARSERS_V1
        if major == 2:
            return DEFAULT_PARSERS_V2
        if major == 4:
            return DEFAULT_PARSERS_V4
        raise ValueError(f"Unsupported MSH format version: {version}")
