"""Parser for MSH 1.0 format nodes ($NOD section).

MSH 1.0 uses the $NOD/$ENDNOD section instead of $Nodes/$EndNodes.
The format is simpler with no entity-based organization.
"""

from typing import TextIO
from .abstract_parser import AbstractParser
from .mesh import Mesh
from .node_entity import NodeEntity
from .node import Node


class NodesParserV1(AbstractParser):
    """Parser for MSH 1.0 $NOD section.

    Format:
    $NOD
    number-of-nodes
    node-number x-coord y-coord z-coord
    ...
    $ENDNOD
    """

    @staticmethod
    def get_section_name():
        return "$NOD"

    @staticmethod
    def parse(mesh: Mesh, io: TextIO) -> None:
        """Parse MSH 1.0 nodes section.

        Parameters
        ----------
        mesh : Mesh
            Mesh object to populate with nodes
        io : TextIO
            Input stream to read from
        """
        # Read number of nodes
        num_nodes = int(io.readline().strip())
        mesh.set_number_of_nodes(num_nodes)

        # Create a single node entity (MSH 1.0 doesn't have entities)
        # Use dimension 2 (surface) and tag 1 as default
        node_entity = NodeEntity()
        node_entity.set_dimension(2)
        node_entity.set_tag(1)
        node_entity.set_number_of_parametric_coordinates(0)
        node_entity.set_number_of_nodes(num_nodes)

        # Read all nodes
        min_tag = float("inf")
        max_tag = 0

        for _ in range(num_nodes):
            line = io.readline().strip().split()
            node_tag = int(line[0])
            x = float(line[1])
            y = float(line[2])
            z = float(line[3])

            # Track min/max tags
            min_tag = min(min_tag, node_tag)
            max_tag = max(max_tag, node_tag)

            # Create node
            node = Node()
            node.set_tag(node_tag)
            node.set_coordinates((x, y, z))
            node_entity.add_node(node)

        # Update mesh with actual min/max tags
        mesh.set_min_node_tag(int(min_tag))
        mesh.set_max_node_tag(int(max_tag))
        mesh.set_number_of_node_entities(1)
        mesh.add_node_entity(node_entity)
