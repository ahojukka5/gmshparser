from typing import Dict, Type, TextIO
from .mesh import Mesh
from .abstract_parser import AbstractParser
from .mesh_format_parser import MeshFormatParser
from .nodes_parser import NodesParser


PARSERS = {
    "$MeshFormat": MeshFormatParser,
    "$Nodes": NodesParser
}


def parse_io(io: TextIO, parsers: Dict[str, Type[AbstractParser]]) -> Mesh:
    """Parse input stream using `parsers` and return `Mesh` object. """
    mesh = Mesh()
    for line in io:
        line = line.strip()
        if not line.startswith("$"):
            continue
        if line.startswith("$End"):
            continue
        if line not in parsers:
            continue
        parsers[line]().parse(mesh, io)
    return mesh


def parse(filename: str) -> Mesh:
    """Parse Gmsh .msh file and return `Mesh` object."""
    with open(filename, "r") as fid:
        return parse_io(fid, PARSERS)
