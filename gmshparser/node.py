from typing import cast


class Node:
    """Node."""

    def __init__(self) -> None:
        self.tag_ = -1
        self.coordinates_ = cast(tuple[float, ...], (None, None, None))

    def set_tag(self, tag: int) -> None:
        """Set node tag (node id)."""
        self.tag_ = tag

    def get_tag(self) -> int:
        """Get node tag (node id)."""
        return self.tag_

    def set_coordinates(self, coordinates: tuple[float, ...]) -> None:
        """Set Cartesian and optional parametric node coordinates."""
        self.coordinates_ = coordinates

    def get_coordinates(self) -> tuple[float, ...]:
        """Get Cartesian and optional parametric node coordinates."""
        return self.coordinates_
