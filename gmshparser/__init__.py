from importlib.metadata import version as _distribution_version

from . import api, helpers
from .api import (
    Element,
    ElementCollection,
    Entity,
    EntityCollection,
    Node,
    NodeCollection,
    PeriodicLink,
    PeriodicLinkCollection,
    PhysicalGroup,
    PhysicalGroupCollection,
    Version,
    read,
)
from .api import (
    Mesh as ModernMesh,
)
from .element_types import ElementFamily, ElementType, ElementTypeInfo
from .errors import (
    GmshError,
    InvalidElementConnectivityError,
    InvalidElementError,
    InvalidMeshError,
    InvalidNodeError,
    InvalidSectionError,
    ParseError,
    ParsingContext,
    UnexpectedEndOfFileError,
    UnknownElementTypeError,
    UnsupportedBinaryFormatError,
    UnsupportedVersionError,
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
    "GmshError",
    "InvalidElementConnectivityError",
    "InvalidElementError",
    "InvalidMeshError",
    "InvalidNodeError",
    "InvalidSectionError",
    "MainParser",
    "Mesh",
    "ModernMesh",
    "MshFormatVersion",
    "Node",
    "NodeCollection",
    "ParseError",
    "ParsingContext",
    "PeriodicLink",
    "PeriodicLinkCollection",
    "PhysicalGroup",
    "PhysicalGroupCollection",
    "UnexpectedEndOfFileError",
    "UnknownElementTypeError",
    "UnsupportedBinaryFormatError",
    "UnsupportedVersionError",
    "Version",
    "VersionManager",
    "api",
    "helpers",
    "parse",
    "read",
]

__version__ = _distribution_version("gmshparser")
__author__ = "Jukka Aho <ahojukka5@gmail.com>"


def parse(filename: str) -> Mesh:
    """Parse a file into the compatibility data model.

    The compatibility model preserves the original ``get_*`` and ``set_*`` API.
    New code should normally use :func:`read`, which returns the modern,
    immutable model from :mod:`gmshparser.api`.
    """
    mesh = Mesh()
    mesh.set_name(filename)
    parser = MainParser()
    with open(filename, encoding="utf-8") as io:
        parser.parse(mesh, io)
    return mesh
