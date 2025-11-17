from typing import List
from .node import Node


class NodeEntity(object):
    """NodeEntity class holds nodes for one block."""

    def __init__(self):
        self.dimension_ = -1
        self.tag_ = -1
        self.number_of_parametric_coordinates_ = -1
        self.number_of_nodes_ = -1
        self.nodes_ = {}

    def set_dimension(self, dimension: int):
        """Set the dimension of the entity to `dimension`."""
        self.dimension_ = dimension

    def get_dimension(self) -> int:
        """Get the dimension of the entity."""
        return self.dimension_

    def set_tag(self, tag: int):
        """Set the tag of the entity."""
        self.tag_ = tag

    def get_tag(self) -> int:
        """Get the tag of the entity."""
        return self.tag_

    def set_number_of_parametric_coordinates(self, npar: int):
        """Set the number of parametric coordinates of the entity."""
        self.number_of_parametric_coordinates_ = npar

    def get_number_of_parametric_coordinates(self) -> int:
        """Get the number of parametric coordinates of the entity."""
        return self.number_of_parametric_coordinates_

    def set_number_of_nodes(self, number_of_nodes: int):
        """Set the number of nodes of the entity."""
        self.number_of_nodes_ = number_of_nodes

    def get_number_of_nodes(self) -> int:
        """Get the number of nodes of the entity."""
        return self.number_of_nodes_

    def add_node(self, node: Node):
        """Add new node to entity."""
        self.nodes_[node.get_tag()] = node

    def get_node(self, tag: int) -> Node:
        """Get node from entity by its tag."""
        return self.nodes_[tag]

    def get_nodes(self) -> List[Node]:
        """Get all nodes in this entity."""
        return self.nodes_.values()
