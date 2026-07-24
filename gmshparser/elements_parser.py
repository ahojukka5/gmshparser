from typing import TextIO

from .abstract_parser import AbstractParser
from .element import Element
from .element_entity import ElementEntity
from .element_types import (
    ElementType,
    validate_element_connectivity,
    validate_element_dimension,
)
from .helpers import parse_ints
from .mesh import Mesh


class ElementsParser(AbstractParser):
    """Parse entity-block elements from MSH 4.x files."""

    @staticmethod
    def get_section_name():
        return "$Elements"

    @staticmethod
    def parse(mesh: Mesh, io: TextIO) -> None:
        line = io.readline()
        if line.startswith("$Elements"):
            line = io.readline()
        metadata = [int(value) for value in line.strip().split()]

        mesh.set_number_of_element_entities(metadata[0])
        mesh.set_number_of_elements(metadata[1])
        mesh.set_min_element_tag(metadata[2])
        mesh.set_max_element_tag(metadata[3])

        for _ in range(mesh.get_number_of_element_entities()):
            block_metadata = parse_ints(io)
            dimension = block_metadata[0]
            entity_tag = block_metadata[1]
            element_type = ElementType(block_metadata[2])
            if element_type.is_known:
                validate_element_dimension(element_type, dimension)
            number_of_elements = block_metadata[3]

            entity = ElementEntity()
            entity.set_dimension(dimension)
            entity.set_tag(entity_tag)
            entity.set_element_type(int(element_type))
            entity.set_number_of_elements(number_of_elements)

            for _ in range(number_of_elements):
                element_info = parse_ints(io)
                element_tag = element_info[0]
                node_tags = element_info[1:]
                if element_type.is_known:
                    validate_element_connectivity(
                        element_type,
                        node_tags,
                        element_tag=element_tag,
                    )

                element = Element()
                element.set_tag(element_tag)
                element.set_connectivity(node_tags)
                entity.add_element(element)

            mesh.add_element_entity(entity)
