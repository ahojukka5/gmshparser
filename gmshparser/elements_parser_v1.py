"""Parser for MSH 1.0 format elements ($ELM section).

MSH 1.0 uses the $ELM/$ENDELM section instead of $Elements/$EndElements.
The element format includes region tags (physical and elementary) directly.
"""

from typing import TextIO

from .abstract_parser import AbstractParser
from .element import Element
from .element_entity import ElementEntity
from .mesh import Mesh


class ElementsParserV1(AbstractParser):
    """Parser for MSH 1.0 $ELM section.

    Format:
    $ELM
    number-of-elements
    elm-number elm-type reg-phys reg-elem number-of-nodes node-number-list
    ...
    $ENDELM
    """

    @staticmethod
    def get_section_name():
        return "$ELM"

    @staticmethod
    def parse(mesh: Mesh, io: TextIO) -> None:
        """Parse MSH 1.0 elements section."""
        num_elements = int(io.readline().strip())
        mesh.set_number_of_elements(num_elements)

        element_groups: dict[tuple[int, int, int], list] = {}
        min_tag = float("inf")
        max_tag = 0

        for _ in range(num_elements):
            line = io.readline().strip().split()

            elm_number = int(line[0])
            elm_type = int(line[1])
            reg_phys = int(line[2])
            reg_elem = int(line[3])
            number_of_nodes = int(line[4])
            node_list = [int(line[5 + i]) for i in range(number_of_nodes)]

            dimension = ElementsParserV1._get_element_dimension(elm_type)
            entity_tag = reg_elem
            physical_tags = (reg_phys,) if reg_phys > 0 else ()

            mesh.set_element_physical_tags(elm_number, physical_tags)
            mesh.add_entity_physical_tags(dimension, entity_tag, physical_tags)

            min_tag = min(min_tag, elm_number)
            max_tag = max(max_tag, elm_number)

            group_key = (dimension, entity_tag, elm_type)
            element_groups.setdefault(group_key, []).append((elm_number, node_list))

        mesh.set_min_element_tag(int(min_tag))
        mesh.set_max_element_tag(int(max_tag))
        mesh.set_number_of_element_entities(len(element_groups))

        for (dimension, entity_tag, element_type), elements in element_groups.items():
            element_entity = ElementEntity()
            element_entity.set_dimension(dimension)
            element_entity.set_tag(entity_tag)
            element_entity.set_element_type(element_type)
            element_entity.set_number_of_elements(len(elements))

            for elm_number, node_list in elements:
                element = Element()
                element.set_tag(elm_number)
                element.set_connectivity(node_list)
                element_entity.add_element(element)

            mesh.add_element_entity(element_entity)

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
