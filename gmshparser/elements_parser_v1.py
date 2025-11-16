"""Parser for MSH 1.0 format elements ($ELM section).

MSH 1.0 uses the $ELM/$ENDELM section instead of $Elements/$EndElements.
The element format includes region tags (physical and elementary) directly.
"""

from typing import TextIO, Dict, Tuple
from .abstract_parser import AbstractParser
from .mesh import Mesh
from .element_entity import ElementEntity
from .element import Element


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
        """Parse MSH 1.0 elements section.

        Parameters
        ----------
        mesh : Mesh
            Mesh object to populate with elements
        io : TextIO
            Input stream to read from
        """
        # Read number of elements
        num_elements = int(io.readline().strip())
        mesh.set_number_of_elements(num_elements)

        # Group elements by (dimension, entity_tag, element_type)
        # In MSH 1.0, reg-elem serves as the entity tag
        element_groups: Dict[Tuple[int, int, int], list] = {}
        min_tag = float("inf")
        max_tag = 0

        # Read all elements
        for _ in range(num_elements):
            line = io.readline().strip().split()

            elm_number = int(line[0])
            elm_type = int(line[1])
            reg_phys = int(line[2])  # Physical entity tag
            reg_elem = int(line[3])  # Elementary entity tag
            number_of_nodes = int(line[4])

            # Get node tags
            # Note: In MSH 1.0, the number of fields may vary depending on element type
            # Line format: elm-number elm-type reg-phys reg-elem number-of-nodes node-list
            node_list = [int(line[5 + i]) for i in range(number_of_nodes)]

            # Get element dimension from type
            dimension = ElementsParserV1._get_element_dimension(elm_type)

            # Use reg_elem as entity tag
            entity_tag = reg_elem

            # Track min/max element tags
            min_tag = min(min_tag, elm_number)
            max_tag = max(max_tag, elm_number)

            # Group key: (dimension, entity_tag, element_type)
            group_key = (dimension, entity_tag, elm_type)

            if group_key not in element_groups:
                element_groups[group_key] = []

            # Add element info to group
            element_groups[group_key].append((elm_number, node_list))

        # Update mesh statistics
        mesh.set_min_element_tag(int(min_tag))
        mesh.set_max_element_tag(int(max_tag))
        mesh.set_number_of_element_entities(len(element_groups))

        # Create element entities from groups
        for (dimension, entity_tag, element_type), elements in element_groups.items():
            element_entity = ElementEntity()
            element_entity.set_dimension(dimension)
            element_entity.set_tag(entity_tag)
            element_entity.set_element_type(element_type)
            element_entity.set_number_of_elements(len(elements))

            for elm_number, node_list in elements:
                # Create element
                element = Element()
                element.set_tag(elm_number)
                element.set_connectivity(node_list)
                element_entity.add_element(element)

            mesh.add_element_entity(element_entity)

    @staticmethod
    def _get_element_dimension(elm_type: int) -> int:
        """Get the dimension of an element based on its type.

        Parameters
        ----------
        elm_type : int
            Element type code

        Returns
        -------
        int
            Dimension (0=point, 1=line, 2=surface, 3=volume)
        """
        # Points
        if elm_type == 15:
            return 0

        # Lines (1st and 2nd order)
        if elm_type in [1, 8, 26, 27, 28]:
            return 1

        # Triangles and quadrangles (1st, 2nd, higher order)
        if elm_type in [2, 3, 9, 10, 16, 20, 21, 22, 23, 24, 25]:
            return 2

        # Tetrahedra, hexahedra, prisms, pyramids (1st, 2nd, higher order)
        if elm_type in [4, 5, 6, 7, 11, 12, 13, 14, 17, 18, 19, 29, 30, 31, 92, 93]:
            return 3

        # Default to 3D if unknown
        return 3
