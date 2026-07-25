class Node:
    """Node."""

    def __init__(self) -> None:
        self.tag_ = -1
        self.coordinates_: tuple[float, float, float] = (0.0, 0.0, 0.0)

    def set_tag(self, tag: int) -> None:
        """Set node tag (node id)."""
        self.tag_ = tag

    def get_tag(self) -> int:
        """Get node tag (node id)."""
        return self.tag_

    def set_coordinates(self, coordinates: tuple[float, float, float]) -> None:
        """Set the coordinates of the node."""
        self.coordinates_ = coordinates

    def get_coordinates(self) -> tuple[float, float, float]:
        """Get the coordinates of the node."""
        return self.coordinates_
