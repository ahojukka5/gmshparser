from typing import Dict, Type, TextIO

from .helpers import parse_ints, parse_floats
from .node import Node
from .node_entity import NodeEntity


class Mesh(object):

    """Mesh is the main class of the package."""

    def __init__(self):
        self.version_ = "unknown"
        self.ascii_ = False
        self.precision_ = -1  # t_size
        self.number_of_entities_ = -1
        self.number_of_nodes_ = -1
        self.min_node_tag_ = -1
        self.max_node_tag_ = -1
        self.entities_ = {}

    def set_version(self, version: str):
        """Set the version of the Mesh object"""
        self.version_ = version

    def get_version(self) -> str:
        """Get the version of the Mesh object"""
        return self.version_

    def set_ascii(self, is_ascii: bool):
        """Set a boolean flag whether this mesh is ASCII or binary"""
        self.ascii_ = is_ascii

    def get_ascii(self) -> bool:
        """Get a boolean flag whether this mesh is ASCII of binary"""
        return self.ascii_

    def set_precision(self, precision: int):
        """Set the precision of the mesh (8)"""
        self.precision_ = precision

    def get_precision(self) -> int:
        """Get the precision of the mesh"""
        return self.precision_

    def set_number_of_entities(self, number_of_entities: int):
        """Set number of entities."""
        self.number_of_entities_ = number_of_entities

    def get_number_of_entities(self) -> int:
        """Get number of entities."""
        return self.number_of_entities_

    def set_number_of_nodes(self, number_of_nodes: int):
        """Set number of nodes."""
        self.number_of_nodes_ = number_of_nodes

    def get_number_of_nodes(self) -> int:
        """Get number of nodes."""
        return self.number_of_nodes_

    def set_min_node_tag(self, min_node_tag: int):
        """Set node minimum tag."""
        self.min_node_tag_ = min_node_tag

    def get_min_node_tag(self) -> int:
        """Get node minimum tag."""
        return self.min_node_tag_

    def set_max_node_tag(self, max_node_tag: int):
        """Set node maximum tag."""
        self.max_node_tag_ = max_node_tag

    def get_max_node_tag(self) -> int:
        """Get node maximum tag."""
        return self.max_node_tag_

    def has_node_entity(self, entity_tag) -> bool:
        """Test does mesh have entity with `entity_tag`."""
        return entity_tag in self.entities_

    def add_node_entity(self, entity: NodeEntity):
        """Add node entity to mesh."""
        self.entities_[entity.get_tag()] = entity

    def get_node_entity(self, tag: int):
        """Get node entity based on tag."""
        return self.entities_[tag]


class AbstractParser(object):
    def parse(self, mesh: Mesh, io: TextIO) -> None:
        raise NotImplementedError(
            "You have to implement parser(self, mesh, io) to your parser")


class MeshFormatParser(AbstractParser):
    def parse(self, mesh: Mesh, io: TextIO) -> None:
        s = io.readline().strip().split(" ")
        mesh.set_version(float(s[0]))
        mesh.set_ascii(int(s[1]) == 0)
        mesh.set_precision(int(s[2]))


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
