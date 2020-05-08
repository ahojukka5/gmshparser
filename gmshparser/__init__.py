from typing import Dict, Type, TextIO
from .mesh import Mesh
from .abstract_parser import AbstractParser
from .mesh_format_parser import MeshFormatParser
from .nodes_parser import NodesParser


Parsers = Dict[str, Type[AbstractParser]]


def parse_io(io: TextIO, mesh: Mesh, parsers: Parsers) -> Mesh:
    """Parse input stream using `parsers` to `mesh` object. """
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


DEFAULT_PARSERS = {
    "$MeshFormat": MeshFormatParser,
    "$Nodes": NodesParser
}


def parse(filename: str, parsers: Parsers = DEFAULT_PARSERS) -> Mesh:
    """Parse Gmsh .msh file and return `Mesh` object."""
    mesh = Mesh()
    mesh.set_name(filename)
    with open(filename, "r") as fid:
        mesh = parse_io(fid, mesh, parsers)
        return mesh
