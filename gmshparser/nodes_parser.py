from typing import TextIO

from .abstract_parser import AbstractParser
from .errors import InvalidNodeError
from .helpers import parse_floats, parse_ints
from .mesh import Mesh
from .parsing import expect_end_marker, read_required_line


class NodesParser(AbstractParser):
    """Parse entity-block nodes from MSH 4.0 and 4.1 files."""

    @staticmethod
    def get_section_name() -> str:
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

        is_v40 = mesh.get_version_major() == 4 and mesh.get_version_minor() == 0
        expected_header_fields = 2 if is_v40 else 4
        if len(metadata) != expected_header_fields:
            raise InvalidNodeError(
                f"$Nodes header for MSH {'4.0' if is_v40 else '4.1'} must contain "
                f"{expected_header_fields} integers"
            )

        if is_v40:
            number_of_entities, number_of_nodes = metadata
            min_tag = max_tag = 0
        else:
            number_of_entities, number_of_nodes, min_tag, max_tag = metadata

        if number_of_entities < 0 or number_of_nodes < 0:
            raise InvalidNodeError("$Nodes counts cannot be negative")

        mesh.set_number_of_node_entities(number_of_entities)
        mesh.set_number_of_nodes(number_of_nodes)
        mesh.set_min_node_tag(min_tag)
        mesh.set_max_node_tag(max_tag)

        parsed_nodes = 0
        parsed_tags: list[int] = []
        for _ in range(number_of_entities):
            entity_metadata = parse_ints(io)
            if len(entity_metadata) != 4:
                raise InvalidNodeError(
                    "A $Nodes entity block header must contain four integers"
                )

            if is_v40:
                entity_tag, dimension, parametric, entity_node_count = entity_metadata
            else:
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

            expected_coordinates = 3 + (dimension if parametric else 0)
            records: list[tuple[int, tuple[float, ...]]] = []

            if is_v40:
                for _ in range(entity_node_count):
                    record = read_required_line(io, "an MSH 4.0 node record")
                    fields = record.strip().split()
                    expected_fields = 1 + expected_coordinates
                    if len(fields) != expected_fields:
                        raise InvalidNodeError(
                            f"An MSH 4.0 node record requires {expected_fields} values, "
                            f"got {len(fields)}"
                        )
                    try:
                        tag = int(fields[0])
                        coordinates = tuple(float(value) for value in fields[1:])
                    except ValueError as error:
                        raise InvalidNodeError(
                            "MSH 4.0 node tags and coordinates must be numeric"
                        ) from error
                    records.append((tag, coordinates))
                    parsed_tags.append(tag)
            else:
                node_tags: list[int] = []
                for _ in range(entity_node_count):
                    tag_line = read_required_line(io, "a node tag")
                    fields = tag_line.strip().split()
                    if len(fields) != 1:
                        raise InvalidNodeError(
                            "Each MSH 4.1 node tag must be on its own line"
                        )
                    try:
                        tag = int(fields[0])
                    except ValueError as error:
                        raise InvalidNodeError("Node tags must be integers") from error
                    node_tags.append(tag)
                    parsed_tags.append(tag)

                for tag in node_tags:
                    coordinate_values = parse_floats(io)
                    if len(coordinate_values) != expected_coordinates:
                        raise InvalidNodeError(
                            f"Node {tag} requires {expected_coordinates} coordinate values, "
                            f"got {len(coordinate_values)}"
                        )
                    records.append((tag, tuple(coordinate_values)))

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

        if is_v40:
            mesh.set_min_node_tag(min(parsed_tags, default=0))
            mesh.set_max_node_tag(max(parsed_tags, default=0))

        expect_end_marker(io, "$EndNodes")
