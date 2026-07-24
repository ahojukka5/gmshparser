"""Parser for Elements section in MSH format version 2.x."""

from typing import TextIO

from .abstract_parser import AbstractParser
from .element import Element
from .element_entity import ElementEntity
from .element_types import validate_element_connectivity
from .mesh import Mesh


class ElementsParserV2(AbstractParser):
    """Parse the flat MSH 2.x ``$Elements`` section."""

    @staticmethod
    def get_section_name():
        return "$Elements"

    @staticmethod
    def parse(mesh: Mesh, io: TextIO) -> None:
        line = io.readline()
        if line.startswith("$Elements"):
            line = io.readline()

        num_elements = int(line.strip())
        mesh.set_number_of_elements(num_elements)

        element_groups: dict[tuple[int, int, int], list[tuple[int, list[int]]]] = {}
        min_tag = float("inf")
        max_tag = 0

        for _ in range(num_elements):
            fields = [int(value) for value in io.readline().strip().split()]

            element_tag = fields[0]
            element_type_id = fields[1]
            num_tags = fields[2]
            tags_start = 3
            tags_end = tags_start + num_tags
            tags = fields[tags_start:tags_end]
            node_tags = fields[tags_end:]

            element_type = validate_element_connectivity(
                element_type_id,
                node_tags,
                element_tag=element_tag,
            )
            dimension = element_type.dimension
            assert dimension is not None

            physical_tags = (tags[0],) if tags and tags[0] > 0 else ()
            entity_tag = tags[1] if len(tags) > 1 else 1

            mesh.set_element_physical_tags(element_tag, physical_tags)
            mesh.add_entity_physical_tags(dimension, entity_tag, physical_tags)

            min_tag = min(min_tag, element_tag)
            max_tag = max(max_tag, element_tag)

            key = (dimension, entity_tag, int(element_type))
            element_groups.setdefault(key, []).append((element_tag, node_tags))

        if num_elements:
            mesh.set_min_element_tag(int(min_tag))
            mesh.set_max_element_tag(int(max_tag))
        mesh.set_number_of_element_entities(len(element_groups))

        for (dimension, entity_tag, element_type), elements in element_groups.items():
            entity = ElementEntity()
            entity.set_dimension(dimension)
            entity.set_tag(entity_tag)
            entity.set_element_type(element_type)
            entity.set_number_of_elements(len(elements))

            for element_tag, node_tags in elements:
                element = Element()
                element.set_tag(element_tag)
                element.set_connectivity(node_tags)
                entity.add_element(element)

            mesh.add_element_entity(entity)
