from typing import Dict, Type, TextIO

from .helpers import parse_ints, parse_floats
from .node import Node
from .node_entity import NodeEntity
from .mesh import Mesh
from .abstract_parser import AbstractParser
from .mesh_format_parser import MeshFormatParser


class NodesParser(AbstractParser):

    def parse(self, mesh: Mesh, io: TextIO) -> None:
        meta = parse_ints(io)
        mesh.set_number_of_entities(meta[0])
        mesh.set_number_of_nodes(meta[1])
        mesh.set_min_node_tag(meta[2])
        mesh.set_max_node_tag(meta[3])
        for i in range(mesh.get_number_of_entities()):
            emeta = parse_ints(io)
            entity = NodeEntity()
            entity.set_dimension(emeta[0])
            entity.set_tag(emeta[1])
            entity.set_number_of_parametric_coordinates(emeta[2])
            entity.set_number_of_nodes(emeta[3])
            node_tags = []
            for j in range(entity.get_number_of_nodes()):
                tag = int(io.readline())
                node = Node()
                node.set_tag(tag)
                node_tags.append(tag)
                entity.add_node(node)
            for tag in node_tags:
                coordinates = parse_floats(io)
                node = entity.get_node(tag)
                node.set_coordinates(tuple(coordinates))
            mesh.add_node_entity(entity)


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
