"""Parser for Nodes section in MSH format version 2.x."""

from typing import TextIO
from .node_entity import NodeEntity
from .node import Node
from .abstract_parser import AbstractParser
from .mesh import Mesh
from .helpers import parse_floats


class NodesParserV2(AbstractParser):
    """Parse Nodes section for MSH format version 2.x.

    In MSH 2.x format, the Nodes section has a simpler structure:
    - First line: number of nodes
    - Following lines: node-number x y z (one per node)

    This is different from MSH 4.x which uses entity blocks.
    """

    @staticmethod
    def get_section_name():
        return "$Nodes"

    @staticmethod
    def parse(mesh: Mesh, io: TextIO) -> None:
        """Parse nodes in MSH 2.x format.

        Format:
            $Nodes
            number-of-nodes
            node-number x-coord y-coord z-coord
            ...
            $EndNodes
        """
        line = io.readline()
        if line.startswith("$Nodes"):
            line = io.readline()

        # Read number of nodes
        num_nodes = int(line.strip())
        mesh.set_number_of_nodes(num_nodes)
        mesh.set_min_node_tag(1)  # Typically starts at 1
        mesh.set_max_node_tag(num_nodes)

        # Create a single node entity for all nodes (dimension 3 for volume)
        # In MSH 2.x, nodes aren't organized by entity blocks
        entity = NodeEntity()
        entity.set_dimension(3)  # Assume 3D
        entity.set_tag(1)
        entity.set_number_of_parametric_coordinates(0)
        entity.set_number_of_nodes(num_nodes)

        # Read each node
        min_tag = float("inf")
        max_tag = 0

        for i in range(num_nodes):
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
            entity.add_node(node)

        # Update mesh with actual min/max tags
        mesh.set_min_node_tag(int(min_tag))
        mesh.set_max_node_tag(int(max_tag))
        mesh.set_number_of_node_entities(1)
        mesh.add_node_entity(entity)
