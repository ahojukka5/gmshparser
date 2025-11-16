"""Parser for Elements section in MSH format version 2.x."""

from typing import TextIO
from .abstract_parser import AbstractParser
from .mesh import Mesh
from .element import Element
from .element_entity import ElementEntity


class ElementsParserV2(AbstractParser):
    """Parse Elements section for MSH format version 2.x.

    In MSH 2.x format, the Elements section has a different structure:
    - First line: number of elements
    - Following lines: elm-number elm-type number-of-tags <tags> node-list

    The tags typically include:
    - tag[0]: physical entity tag
    - tag[1]: elementary entity tag
    - tag[2+]: partition information (optional)
    """

    @staticmethod
    def get_section_name():
        return "$Elements"

    @staticmethod
    def parse(mesh: Mesh, io: TextIO) -> None:
        """Parse elements in MSH 2.x format.

        Format:
            $Elements
            number-of-elements
            elm-number elm-type number-of-tags tag... node-number-list
            ...
            $EndElements
        """
        line = io.readline()
        if line.startswith("$Elements"):
            line = io.readline()

        # Read number of elements
        num_elements = int(line.strip())
        mesh.set_number_of_elements(num_elements)

        # Group elements by (dimension, entity_tag, element_type)
        # This allows us to organize MSH 2.x flat structure into MSH 4.x entity blocks
        element_groups = {}
        min_tag = float("inf")
        max_tag = 0

        for i in range(num_elements):
            parts = list(map(int, io.readline().strip().split()))

            elm_number = parts[0]
            elm_type = parts[1]
            num_tags = parts[2]

            # Extract tags
            tags_start = 3
            tags_end = tags_start + num_tags
            tags = parts[tags_start:tags_end]

            # Extract node connectivity
            node_list = parts[tags_end:]

            # Determine entity tag (use elementary entity tag if available)
            entity_tag = tags[1] if len(tags) > 1 else 1

            # Determine dimension from element type
            dimension = ElementsParserV2._get_element_dimension(elm_type)

            # Track min/max element tags
            min_tag = min(min_tag, elm_number)
            max_tag = max(max_tag, elm_number)

            # Group key
            key = (dimension, entity_tag, elm_type)

            if key not in element_groups:
                element_groups[key] = []

            element_groups[key].append((elm_number, node_list))

        # Update mesh statistics
        mesh.set_min_element_tag(int(min_tag))
        mesh.set_max_element_tag(int(max_tag))
        mesh.set_number_of_element_entities(len(element_groups))

        # Create element entities from groups
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
