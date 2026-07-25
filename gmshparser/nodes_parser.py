from typing import TextIO

from .abstract_parser import AbstractParser
from .errors import InvalidNodeError
from .helpers import parse_floats, parse_ints
from .mesh import Mesh
from .parsing import expect_end_marker, read_required_line


class NodesParser(AbstractParser):
    """Parse entity-block nodes from MSH 4.x files."""

    @staticmethod
    def get_section_name():
        return "$Nodes"

    @staticmethod
    def parse(mesh: Mesh, io: TextIO) -> None:
        line = read_required_line(io, "$Nodes header")
        if line.startswith("$Nodes"):
            line = read_required_line(io, "$Nodes header")

        try:
            metadata = [int(value) for value in line.strip().split()]
        except ValueError as error:
            raise InvalidNodeError("$Nodes header must contain integers") from error
        if len(metadata) != 4:
            raise InvalidNodeError("$Nodes header must contain four integers")

        number_of_entities, number_of_nodes, min_tag, max_tag = metadata
        if number_of_entities < 0 or number_of_nodes < 0:
            raise InvalidNodeError("$Nodes counts cannot be negative")

        mesh.set_number_of_node_entities(number_of_entities)
        mesh.set_number_of_nodes(number_of_nodes)
        mesh.set_min_node_tag(min_tag)
        mesh.set_max_node_tag(max_tag)

        parsed_nodes = 0
        for _ in range(number_of_entities):
            entity_metadata = parse_ints(io)
            if len(entity_metadata) != 4:
                raise InvalidNodeError(
                    "A $Nodes entity block header must contain four integers"
                )

            dimension, entity_tag, parametric, entity_node_count = entity_metadata
            if dimension not in {0, 1, 2, 3}:
                raise InvalidNodeError(
                    f"Node entity {entity_tag} has invalid dimension {dimension}"
                )
            if parametric not in {0, 1}:
                raise InvalidNodeError(
                    f"Node entity {entity_tag} has invalid parametric flag {parametric}"
                )
            if entity_node_count < 0:
                raise InvalidNodeError("Node entity counts cannot be negative")

            node_tags: list[int] = []
            for _ in range(entity_node_count):
                tag_line = read_required_line(io, "a node tag")
                fields = tag_line.strip().split()
                if len(fields) != 1:
                    raise InvalidNodeError(
                        "Each MSH 4 node tag must be on its own line"
                    )
                try:
                    node_tags.append(int(fields[0]))
                except ValueError as error:
                    raise InvalidNodeError("Node tags must be integers") from error

            expected_coordinates = 3 + (dimension if parametric else 0)
            records: list[tuple[int, tuple[float, ...]]] = []
            for tag in node_tags:
                coordinates = parse_floats(io)
                if len(coordinates) != expected_coordinates:
                    raise InvalidNodeError(
                        f"Node {tag} requires {expected_coordinates} coordinate values, "
                        f"got {len(coordinates)}"
                    )
                records.append((tag, tuple(coordinates)))

            parsed_nodes += entity_node_count
            mesh.add_node_block(
                dimension,
                entity_tag,
                dimension if parametric else 0,
                records,
            )

        if parsed_nodes != number_of_nodes:
            raise InvalidNodeError(
                f"$Nodes declares {number_of_nodes} nodes, parsed {parsed_nodes}"
            )
        expect_end_marker(io, "$EndNodes")
