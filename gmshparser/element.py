from typing import List


class Element(object):

    """ Element. """

    def __init__(self):
        self.tag_ = -1
        self.connectivity_ = []

    def set_tag(self, tag: int):
        """Set element tag."""
        self.tag_ = tag

    def get_tag(self):
        """Get element tag."""
        return self.tag_

    def set_connectivity(self, connectivity: List[int]):
        """Set element connectivity."""
        self.connectivity_ = connectivity

    def get_connectivity(self) -> List[int]:
        """Get element connectivity."""
        return self.connectivity_
