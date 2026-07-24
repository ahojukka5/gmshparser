"""Parser for Elements section in MSH format version 2.x."""

from typing import TextIO

from .abstract_parser import AbstractParser
from .element import Element
from .element_entity import ElementEntity
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

        element_groups = {}
        min_tag = float("inf")
        max_tag = 0

        for _ in range(num_elements):
            parts = list(map(int, io.readline().strip().split()))

            elm_number = parts[0]
            elm_type = parts[1]
            num_tags = parts[2]
            tags_start = 3
            tags_end = tags_start + num_tags
            tags = parts[tags_start:tags_end]
            node_list = parts[tags_end:]

            physical_tags = (tags[0],) if tags and tags[0] > 0 else ()
            entity_tag = tags[1] if len(tags) > 1 else 1
            dimension = ElementsParserV2._get_element_dimension(elm_type)

            mesh.set_element_physical_tags(elm_number, physical_tags)
            mesh.add_entity_physical_tags(dimension, entity_tag, physical_tags)

            min_tag = min(min_tag, elm_number)
            max_tag = max(max_tag, elm_number)

            key = (dimension, entity_tag, elm_type)
            element_groups.setdefault(key, []).append((elm_number, node_list))

        mesh.set_min_element_tag(int(min_tag))
        mesh.set_max_element_tag(int(max_tag))
        mesh.set_number_of_element_entities(len(element_groups))

        for (dimension, entity_tag, elm_type), elements in element_groups.items():
            entity = ElementEntity()
            entity.set_dimension(dimension)
            entity.set_tag(entity_tag)
            entity.set_element_type(elm_type)
            entity.set_number_of_elements(len(elements))

            for elm_number, node_list in elements:
                element = Element()
                element.set_tag(elm_number)
                element.set_connectivity(node_list)
                entity.add_element(element)

            mesh.add_element_entity(entity)

    @staticmethod
    def _get_element_dimension(elm_type: int) -> int:
        """Get the topological dimension for a numeric Gmsh element type."""
        if elm_type == 15:
            return 0
        if elm_type in [1, 8, 26, 27, 28]:
            return 1
        if elm_type in [2, 3, 9, 10, 16, 20, 21, 22, 23, 24, 25]:
            return 2
        if elm_type in [4, 5, 6, 7, 11, 12, 13, 14, 17, 18, 19, 29, 30, 31, 92, 93]:
            return 3
        return 3
