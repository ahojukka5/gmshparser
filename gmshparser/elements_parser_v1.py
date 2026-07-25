"""Parser for MSH 1.0 format elements (``$ELM`` section)."""

from typing import TextIO

from .abstract_parser import AbstractParser
from .element_types import (
    InvalidElementConnectivityError,
    validate_element_connectivity,
)
from .errors import InvalidElementError
from .mesh import Mesh
from .parsing import expect_end_marker, read_required_line


class ElementsParserV1(AbstractParser):
    """Parse the legacy MSH 1.0 ``$ELM`` section."""

    @staticmethod
    def get_section_name():
        return "$ELM"

    @staticmethod
    def parse(mesh: Mesh, io: TextIO) -> None:
        count_line = read_required_line(io, "$ELM element count")
        try:
            number_of_elements = int(count_line.strip())
        except ValueError as error:
            raise InvalidElementError(
                "$ELM element count must be an integer"
            ) from error
        if number_of_elements < 0:
            raise InvalidElementError("$ELM element count cannot be negative")

        mesh.set_number_of_elements(number_of_elements)
        element_groups: dict[
            tuple[int, int, int],
            list[tuple[int, list[int], tuple[int, ...]]],
        ] = {}
        physical_tags_by_entity: dict[tuple[int, int], list[int]] = {}
        min_tag: int | None = None
        max_tag: int | None = None

        for _ in range(number_of_elements):
            line = read_required_line(io, "an MSH 1 element record")
            fields = line.strip().split()
            if len(fields) < 5:
                raise InvalidElementError(
                    "An MSH 1 element record must contain at least five fields"
                )

            try:
                element_tag = int(fields[0])
                element_type_id = int(fields[1])
                physical_tag = int(fields[2])
                entity_tag = int(fields[3])
                declared_node_count = int(fields[4])
                node_tags = [int(value) for value in fields[5:]]
            except ValueError as error:
                raise InvalidElementError(
                    "MSH 1 element records must contain integers"
                ) from error

            if declared_node_count < 0:
                raise InvalidElementError("Declared node counts cannot be negative")
            if len(node_tags) != declared_node_count:
                raise InvalidElementConnectivityError(
                    f"Element {element_tag} declares {declared_node_count} nodes, "
                    f"but the record contains {len(node_tags)}"
                )

            element_type = validate_element_connectivity(
                element_type_id,
                node_tags,
                element_tag=element_tag,
            )
            dimension = element_type.dimension
            assert dimension is not None

            physical_tags = (physical_tag,) if physical_tag > 0 else ()
            entity_key = dimension, entity_tag
            if physical_tag > 0:
                entity_tags = physical_tags_by_entity.setdefault(entity_key, [])
                if physical_tag not in entity_tags:
                    entity_tags.append(physical_tag)

            min_tag = element_tag if min_tag is None else min(min_tag, element_tag)
            max_tag = element_tag if max_tag is None else max(max_tag, element_tag)
            block_key = (dimension, entity_tag, int(element_type))
            element_groups.setdefault(block_key, []).append(
                (element_tag, node_tags, physical_tags)
            )

        if min_tag is not None and max_tag is not None:
            mesh.set_min_element_tag(min_tag)
            mesh.set_max_element_tag(max_tag)
        mesh.set_number_of_element_entities(len(element_groups))

        for (
            dimension,
            entity_tag,
        ), entity_physical_tags in physical_tags_by_entity.items():
            mesh.add_entity_physical_tags(
                dimension,
                entity_tag,
                entity_physical_tags,
            )
        for (dimension, entity_tag, type_id), block_elements in element_groups.items():
            mesh.add_element_block(dimension, entity_tag, type_id, block_elements)

        expect_end_marker(io, "$ENDELM")
