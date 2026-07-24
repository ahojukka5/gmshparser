from .mesh import Mesh
from .main_parser import MainParser
from .version_manager import VersionManager, MshFormatVersion
from . import helpers

__all__ = [
    "MainParser",
    "Mesh",
    "MshFormatVersion",
    "VersionManager",
    "helpers",
    "parse",
]

__version__ = "0.3.1"
__author__ = "Jukka Aho <ahojukka5@gmail.com>"


def parse(filename: str) -> Mesh:
    """Parse an ASCII Gmsh MSH file and return a :class:`Mesh` object.

    The file format version is detected automatically. Supported versions are
    MSH 1.0, 2.0, 2.1, 2.2, 4.0, and 4.1.

    Parameters
    ----------
    filename : str
        Path to the MSH file.

    Returns
    -------
    Mesh
        Parsed mesh containing nodes, elements, and format metadata.

    Raises
    ------
    FileNotFoundError
        If the file does not exist.
    ValueError
        If the MSH version is unsupported or the input is invalid.
    """
    mesh = Mesh()
    mesh.set_name(filename)
    parser = MainParser()
    with open(filename, "r") as io:
        parser.parse(mesh, io)
    return mesh
