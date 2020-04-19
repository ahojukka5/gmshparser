from typing import Tuple


class Node(object):

    """ Node. """

    def __init__(self):
        self.tag_ = -1
        self.coordinates_ = (None, None, None)

    def set_tag(self, tag: int):
        """Set node tag (node id)."""
        self.tag_ = tag

    def get_tag(self) -> int:
        """Get node tag (node id)."""
        return self.tag_

    def set_coordinates(self, coordinates: Tuple[float, float, float]):
        """Set the coordinates of the node."""
        self.coordinates_ = coordinates

    def get_coordinates(self) -> Tuple[float, float, float]:
        """Get the coordinates of the node."""
        return self.coordinates_
