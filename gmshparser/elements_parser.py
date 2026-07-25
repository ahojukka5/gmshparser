from typing import TextIO

from .abstract_parser import AbstractParser
from .element_types import (
    ElementType,
    validate_element_connectivity,
    validate_element_dimension,
)
from .errors import InvalidElementError
from .helpers import parse_ints
from .mesh import Mesh
from .parsing import expect_end_marker, read_required_line


class ElementsParser(AbstractParser):
    """Parse entity-block elements from MSH 4.0 and 4.1 files."""

    @staticmethod
    def get_section_name() -> str:
        return "$Elements"

    @staticmethod
    def parse(mesh: Mesh, io: TextIO) -> None:
        line = read_required_line(io, "$Elements header")
        if line.startswith("$Elements"):
            line = read_required_line(io, "$Elements header")

        try:
            metadata = [int(value) for value in line.strip().split()]
        except ValueError as error:
            raise InvalidElementError(
                "$Elements header must contain integers"
            ) from error

        is_v40 = mesh.get_version_major() == 4 and mesh.get_version_minor() == 0
        expected_header_fields = 2 if is_v40 else 4
        if len(metadata) != expected_header_fields:
            raise InvalidElementError(
                f"$Elements header for MSH {'4.0' if is_v40 else '4.1'} must "
                f"contain {expected_header_fields} integers"
            )

        if is_v40:
            number_of_entities, number_of_elements = metadata
            min_tag = max_tag = 0
        else:
            number_of_entities, number_of_elements, min_tag, max_tag = metadata

        if number_of_entities < 0 or number_of_elements < 0:
            raise InvalidElementError("$Elements counts cannot be negative")

        mesh.set_number_of_element_entities(number_of_entities)
        mesh.set_number_of_elements(number_of_elements)
        mesh.set_min_element_tag(min_tag)
        mesh.set_max_element_tag(max_tag)

        parsed_elements = 0
        parsed_tags: list[int] = []
        for _ in range(number_of_entities):
            block_metadata = parse_ints(io)
            if len(block_metadata) != 4:
                raise InvalidElementError(
                    "An $Elements block header must contain four integers"
                )

            if is_v40:
                entity_tag, dimension, type_id, block_count = block_metadata
            else:
                dimension, entity_tag, type_id, block_count = block_metadata

            if dimension not in {0, 1, 2, 3}:
                raise InvalidElementError(
                    f"Element entity {entity_tag} has invalid dimension {dimension}"
                )
            if block_count < 0:
                raise InvalidElementError("Element block counts cannot be negative")

            element_type = ElementType(type_id)
            if element_type.is_known:
                validate_element_dimension(element_type, dimension)

            records: list[tuple[int, list[int], tuple[int, ...]]] = []
            for _ in range(block_count):
                element_info = parse_ints(io)
                if not element_info:
                    raise InvalidElementError("An element record cannot be empty")
                element_tag = element_info[0]
                node_tags = element_info[1:]
                if element_type.is_known:
                    validate_element_connectivity(
                        element_type,
                        node_tags,
                        element_tag=element_tag,
                    )
                records.append((element_tag, node_tags, ()))
                parsed_tags.append(element_tag)

            parsed_elements += block_count
            mesh.add_element_block(
                dimension,
                entity_tag,
                int(element_type),
                records,
            )

        if parsed_elements != number_of_elements:
            raise InvalidElementError(
                f"$Elements declares {number_of_elements} elements, "
                f"parsed {parsed_elements}"
            )

        if is_v40:
            mesh.set_min_element_tag(min(parsed_tags, default=0))
            mesh.set_max_element_tag(max(parsed_tags, default=0))

        expect_end_marker(io, "$EndElements")
