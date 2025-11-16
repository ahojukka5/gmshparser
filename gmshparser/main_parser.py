from typing import TextIO, List, Type
from .mesh import Mesh
from .mesh_format_parser import MeshFormatParser
from .nodes_parser import NodesParser
from .nodes_parser_v1 import NodesParserV1
from .nodes_parser_v2 import NodesParserV2
from .elements_parser import ElementsParser
from .elements_parser_v1 import ElementsParserV1
from .elements_parser_v2 import ElementsParserV2
from .abstract_parser import AbstractParser
from .version_manager import VersionManager, MshFormatVersion


# Default parsers for MSH 4.x format
DEFAULT_PARSERS_V4 = [
    MeshFormatParser,
    NodesParser,
    ElementsParser,
]

# Default parsers for MSH 2.x format
DEFAULT_PARSERS_V2 = [
    MeshFormatParser,
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

            # Check for MSH 1.0 format (starts with $NOD instead of $MeshFormat)
            if line == "$NOD" and not self.version_detected:
                # Set version to 1.0
                mesh.set_version(1.0)
                self.version_detected = True

                # Select MSH 1.0 parsers
                if self.parsers is None:
                    self.parsers = DEFAULT_PARSERS_V1

                # Parse the $NOD section
                try:
                    NodesParserV1.parse(mesh, io)
                except Exception:
                    print("Unable to parse section %s from mesh!" % line)
                    raise
                continue

            # Handle MeshFormat for MSH 2.x and 4.x
            if line == "$MeshFormat" and not self.version_detected:
                try:
                    MeshFormatParser.parse(mesh, io)
                    self.version_detected = True

                    # Select parsers based on detected version if not explicitly set
                    if self.parsers is None:
                        self.parsers = self._get_parsers_for_version(mesh)

                except Exception:
                    print("Unable to parse section %s from mesh!" % line)
                    raise
                continue

            # Then, handle other sections with version-specific parsers
            if self.parsers:
                for parser in self.parsers:
                    if parser.get_section_name() == line:
                        try:
                            parser.parse(mesh, io)
                        except Exception:
                            print("Unable to parse section %s from mesh!" % line)
                            raise
                        break

    def _get_parsers_for_version(self, mesh: Mesh) -> List[Type[AbstractParser]]:
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
        elif major == 2:
            return DEFAULT_PARSERS_V2
        elif major == 4:
            return DEFAULT_PARSERS_V4
        else:
            raise ValueError(f"Unsupported MSH format version: {version}")
