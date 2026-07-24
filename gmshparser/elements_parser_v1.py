"""Parser for MSH 1.0 format elements ($ELM section).

MSH 1.0 uses the $ELM/$ENDELM section instead of $Elements/$EndElements.
The element format includes region tags (physical and elementary) directly.
"""

from typing import TextIO

from .abstract_parser import AbstractParser
from .element import Element
from .element_entity import ElementEntity
from .element_types import (
    InvalidElementConnectivityError,
    validate_element_connectivity,
)
from .mesh import Mesh


class ElementsParserV1(AbstractParser):
    """Parser for the legacy MSH 1.0 ``$ELM`` section."""

    @staticmethod
    def get_section_name():
        return "$ELM"

    @staticmethod
    def parse(mesh: Mesh, io: TextIO) -> None:
        """Parse MSH 1.0 element records into compatibility entities."""
        num_elements = int(io.readline().strip())
        mesh.set_number_of_elements(num_elements)

        element_groups: dict[tuple[int, int, int], list[tuple[int, list[int]]]] = {}
        min_tag = float("inf")
        max_tag = 0

        for _ in range(num_elements):
            fields = io.readline().strip().split()

            element_tag = int(fields[0])
            element_type_id = int(fields[1])
            physical_tag = int(fields[2])
            entity_tag = int(fields[3])
            declared_node_count = int(fields[4])
            node_tags = [int(value) for value in fields[5:]]

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
