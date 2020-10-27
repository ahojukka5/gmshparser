from typing import TextIO
from .node_entity import NodeEntity
from .node import Node
from .abstract_parser import AbstractParser
from .mesh import Mesh
from .helpers import parse_ints, parse_floats


class NodesParser(AbstractParser):
    """Parse Nodes section."""

    @staticmethod
    def get_section_name():
        return "$Nodes"

    @staticmethod
    def parse(mesh: Mesh, io: TextIO) -> None:
        line = io.readline()
        if line.startswith("$Nodes"):
            line = io.readline()
        meta = list(map(int, line.strip().split(" ")))

        mesh.set_number_of_node_entities(meta[0])
        mesh.set_number_of_nodes(meta[1])
        mesh.set_min_node_tag(meta[2])
        mesh.set_max_node_tag(meta[3])
        for i in range(mesh.get_number_of_node_entities()):
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
