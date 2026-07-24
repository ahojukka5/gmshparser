"""Parser for MSH 1.0 format nodes (``$NOD`` section)."""

from typing import TextIO

from .abstract_parser import AbstractParser
from .errors import InvalidNodeError
from .mesh import Mesh
from .node import Node
from .node_entity import NodeEntity
from .parsing import expect_end_marker, read_required_line


class NodesParserV1(AbstractParser):
    """Parse the legacy MSH 1.0 ``$NOD`` section."""

    @staticmethod
    def get_section_name():
        return "$NOD"

    @staticmethod
    def parse(mesh: Mesh, io: TextIO) -> None:
        count_line = read_required_line(io, "$NOD node count")
        try:
            number_of_nodes = int(count_line.strip())
        except ValueError as error:
            raise InvalidNodeError("$NOD node count must be an integer") from error
        if number_of_nodes < 0:
            raise InvalidNodeError("$NOD node count cannot be negative")

        mesh.set_number_of_nodes(number_of_nodes)

        entity = NodeEntity()
        entity.set_dimension(2)
        entity.set_tag(1)
        entity.set_number_of_parametric_coordinates(0)
        entity.set_number_of_nodes(number_of_nodes)

        min_tag: int | None = None
        max_tag: int | None = None
        for _ in range(number_of_nodes):
            line = read_required_line(io, "an MSH 1 node record")
            fields = line.strip().split()
            if len(fields) != 4:
                raise InvalidNodeError(
                    "An MSH 1 node record must contain tag, x, y, and z"
                )
            try:
                node_tag = int(fields[0])
                coordinates = tuple(float(value) for value in fields[1:])
            except ValueError as error:
                raise InvalidNodeError(
                    "MSH 1 node tags and coordinates must be numeric"
                ) from error

            min_tag = node_tag if min_tag is None else min(min_tag, node_tag)
            max_tag = node_tag if max_tag is None else max(max_tag, node_tag)

            node = Node()
            node.set_tag(node_tag)
            node.set_coordinates(coordinates)
            entity.add_node(node)

        if min_tag is not None and max_tag is not None:
            mesh.set_min_node_tag(min_tag)
            mesh.set_max_node_tag(max_tag)
        mesh.set_number_of_node_entities(1)
        mesh.add_node_entity(entity)
        expect_end_marker(io, "$ENDNOD")
