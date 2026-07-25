class Element:
    """Element."""

    def __init__(self) -> None:
        self.tag_ = -1
        self.connectivity_: list[int] = []

    def set_tag(self, tag: int) -> None:
        """Set element tag."""
        self.tag_ = tag

    def get_tag(self) -> int:
        """Get element tag."""
        return self.tag_

    def set_connectivity(self, connectivity: list[int]) -> None:
        """Set element connectivity."""
        self.connectivity_ = connectivity

    def get_connectivity(self) -> list[int]:
        """Get element connectivity."""
        return self.connectivity_
