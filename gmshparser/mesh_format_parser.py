from typing import TextIO
from .abstract_parser import AbstractParser
from .mesh import Mesh
from .version_manager import VersionManager


class MeshFormatParser(AbstractParser):
    """Parse MeshFormat section.

    This parser detects and validates the MSH format version and stores it
    in the mesh object. The version information is then used by the MainParser
    to select appropriate parsers for the rest of the file.
    """

    @staticmethod
    def get_section_name():
        return "$MeshFormat"

    @staticmethod
    def parse(mesh: Mesh, io: TextIO) -> None:
        """Parse the MeshFormat section and validate version.

        Parameters
        ----------
        mesh : Mesh
            Mesh object to store the format information
        io : TextIO
            Input stream to read from

        Raises
        ------
        ValueError
            If the version is not supported or cannot be parsed
        """
        s = io.readline().strip().split(" ")

        # Parse version
        version_str = s[0]
        version_enum = VersionManager.validate_version(version_str)

        # Set version in mesh
        mesh.set_version(version_enum.version_number)

        # Parse format type (0 = ASCII, 1 = binary)
        mesh.set_ascii(int(s[1]) == 0)

        # Parse precision (size of floating point numbers)
        mesh.set_precision(int(s[2]))
