from . import api, helpers
from .api import (
    Element,
    ElementCollection,
    Entity,
    EntityCollection,
    Node,
    NodeCollection,
    PhysicalGroup,
    PhysicalGroupCollection,
    Version,
    read,
)
from .api import (
    Mesh as ModernMesh,
)
from .element_types import (
    ElementFamily,
    ElementType,
    ElementTypeInfo,
    InvalidElementConnectivityError,
    UnknownElementTypeError,
)
from .main_parser import MainParser
from .mesh import Mesh
from .version_manager import MshFormatVersion, VersionManager

__all__ = [
    "Element",
    "ElementCollection",
    "ElementFamily",
    "ElementType",
    "ElementTypeInfo",
    "Entity",
    "EntityCollection",
    "InvalidElementConnectivityError",
    "MainParser",
    "Mesh",
    "ModernMesh",
    "MshFormatVersion",
    "Node",
    "NodeCollection",
    "PhysicalGroup",
    "PhysicalGroupCollection",
    "UnknownElementTypeError",
    "Version",
    "VersionManager",
    "api",
    "helpers",
    "parse",
    "read",
]

__version__ = "0.3.1"
__author__ = "Jukka Aho <ahojukka5@gmail.com>"


def parse(filename: str) -> Mesh:
    """Parse a file into the compatibility data model.

    The compatibility model preserves the original ``get_*`` and ``set_*`` API.
    New code should normally use :func:`read`, which returns the modern,
    immutable model from :mod:`gmshparser.api`.

    Parameters
    ----------
    filename : str
        Path to an ASCII Gmsh MSH file.

    Returns
    -------
    Mesh
        Compatibility mesh containing parser-oriented entities.

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
    with open(filename) as io:
        parser.parse(mesh, io)
    return mesh
