from .mesh import Mesh
from .main_parser import MainParser
from .version_manager import VersionManager, MshFormatVersion
from . import helpers

__version__ = "0.2.0"
__author__ = "Jukka Aho <ahojukka5@gmail.com>"


def parse(filename: str) -> Mesh:
    """Parse Gmsh .msh file and return `Mesh` object.

    This function automatically detects the MSH format version and uses
    the appropriate parsers for that version.

    Supported versions:
    - MSH 2.2 (legacy format)
    - MSH 4.0
    - MSH 4.1 (current format)

    Parameters
    ----------
    filename : str
        Path to the .msh file to parse

    Returns
    -------
    Mesh
        Parsed mesh object containing nodes, elements, and metadata

    Raises
    ------
    ValueError
        If the file version is not supported
    FileNotFoundError
        If the file does not exist
    """
    mesh = Mesh()
    mesh.set_name(filename)
    parser = MainParser()
    with open(filename, "r") as io:
        parser.parse(mesh, io)
    return mesh
