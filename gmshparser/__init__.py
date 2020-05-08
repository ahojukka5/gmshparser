from typing import TextIO
from .mesh import Mesh
from .mesh_format_parser import MeshFormatParser
from .nodes_parser import NodesParser
from .elements_parser import ElementsParser


DEFAULT_PARSERS = {
    "$MeshFormat": MeshFormatParser,
    "$Nodes": NodesParser,
    "$Elements": ElementsParser,
}


def parse_io(io: TextIO, mesh=Mesh(), parsers=DEFAULT_PARSERS) -> Mesh:
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


def parse(filename: str) -> Mesh:
    """Parse Gmsh .msh file and return `Mesh` object."""
    with open(filename, "r") as fid:
        mesh = parse_io(fid)
        mesh.set_name(filename)
        return mesh
