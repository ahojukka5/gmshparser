from collections.abc import ValuesView
from io import StringIO

from .element import Element


class ElementEntity:
    """ElementEntity class holds elements for one block."""

    def __init__(self) -> None:
        self.dimension_ = -1
        self.tag_ = -1
        self.element_type_ = -1
        self.number_of_elements_ = -1
        self.elements_: dict[int, Element] = {}

    def set_dimension(self, dimension: int) -> None:
        """Set the dimension of element entity."""
        self.dimension_ = dimension

    def get_dimension(self) -> int:
        """Get the dimension of the element entity."""
        return self.dimension_

    def set_tag(self, tag: int) -> None:
        """Set the tag of the element entity."""
        self.tag_ = tag

    def get_tag(self) -> int:
        """Get the tag of the element entity."""
        return self.tag_

    def set_element_type(self, element_type: int) -> None:
        """Set element type in element entity."""
        self.element_type_ = element_type

    def get_element_type(self) -> int:
        """Get element type in element entity."""
        return self.element_type_

    def set_number_of_elements(self, number_of_elements: int) -> None:
        """Set the number of elements in entity."""
        self.number_of_elements_ = number_of_elements

    def get_number_of_elements(self) -> int:
        """Get the number of elements in entity."""
        return self.number_of_elements_

    def add_element(self, element: Element) -> None:
        """Add a new element to the entity."""
        self.elements_[element.get_tag()] = element

    def get_element(self, tag: int) -> Element:
        """Get an element from the entity."""
        return self.elements_[tag]

    def get_elements(self) -> ValuesView[Element]:
        """Return all the elements of this entity."""
        return self.elements_.values()

    def __str__(self) -> str:
        io = StringIO()
        io.write(f"---- Element entity # {self.get_tag()} ----\n")
        io.write(f"Dimension: {self.get_dimension()}\n")
        io.write(f"Element type: {self.get_element_type()}\n")
        io.write(f"Number of elements: {self.get_number_of_elements()}\n")
        return io.getvalue()
