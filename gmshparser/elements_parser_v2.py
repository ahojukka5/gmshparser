"""Parser for the MSH 2.x ``$Elements`` section."""

from typing import TextIO

from .abstract_parser import AbstractParser
from .element_types import validate_element_connectivity
from .errors import InvalidElementError
from .mesh import Mesh
from .parsing import expect_end_marker, read_required_line


class ElementsParserV2(AbstractParser):
    """Parse flat MSH 2.x element records."""

    @staticmethod
    def get_section_name():
        return "$Elements"

    @staticmethod
    def parse(mesh: Mesh, io: TextIO) -> None:
        line = read_required_line(io, "$Elements element count")
        if line.startswith("$Elements"):
            line = read_required_line(io, "$Elements element count")

        try:
            number_of_elements = int(line.strip())
        except ValueError as error:
            raise InvalidElementError(
                "$Elements element count must be an integer"
            ) from error
        if number_of_elements < 0:
            raise InvalidElementError("$Elements element count cannot be negative")

        mesh.set_number_of_elements(number_of_elements)
        element_groups: dict[
            tuple[int, int, int],
            list[tuple[int, list[int], tuple[int, ...]]],
        ] = {}
        physical_tags_by_entity: dict[tuple[int, int], list[int]] = {}
        min_tag: int | None = None
        max_tag: int | None = None

        for _ in range(number_of_elements):
            record = read_required_line(io, "an MSH 2 element record")
            try:
                fields = [int(value) for value in record.strip().split()]
            except ValueError as error:
                raise InvalidElementError(
                    "MSH 2 element records must contain integers"
                ) from error
            if len(fields) < 3:
                raise InvalidElementError(
                    "An MSH 2 element record must contain at least three fields"
                )

            element_tag = fields[0]
            element_type_id = fields[1]
            number_of_tags = fields[2]
            if number_of_tags < 0:
                raise InvalidElementError("Element tag counts cannot be negative")

            tags_start = 3
            tags_end = tags_start + number_of_tags
            if len(fields) < tags_end:
                raise InvalidElementError(
                    f"Element {element_tag} declares {number_of_tags} tags, "
                    f"but the record contains {max(0, len(fields) - tags_start)}"
                )

            tags = fields[tags_start:tags_end]
            node_tags = fields[tags_end:]
            element_type = validate_element_connectivity(
                element_type_id,
                node_tags,
                element_tag=element_tag,
            )
            dimension = element_type.dimension
            assert dimension is not None

            physical_tag = tags[0] if tags and tags[0] > 0 else 0
            physical_tags = (physical_tag,) if physical_tag else ()
            entity_tag = tags[1] if len(tags) > 1 else 1
            entity_key = dimension, entity_tag
            if physical_tag:
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

        for (dimension, entity_tag), entity_physical_tags in physical_tags_by_entity.items():
            mesh.add_entity_physical_tags(
                dimension,
                entity_tag,
                entity_physical_tags,
            )
        for (dimension, entity_tag, type_id), block_elements in element_groups.items():
            mesh.add_element_block(dimension, entity_tag, type_id, block_elements)

        expect_end_marker(io, "$EndElements")
