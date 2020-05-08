from typing import List
from io import StringIO
from .element import Element


class ElementEntity(object):

    """ ElementEntity class holds elements for one block. """

    def __init__(self):
        self.dimension_ = -1
        self.tag_ = -1
        self.element_type_ = -1
        self.number_of_elements_ = -1
        self.elements_ = {}

    def set_dimension(self, dimension: int):
        """Set the dimension of element entity."""
        self.dimension_ = dimension

    def get_dimension(self) -> int:
        """Get the dimension of the element entity."""
        return self.dimension_

    def set_tag(self, tag: int):
        """Set the tag of the element entity."""
        self.tag_ = tag

    def get_tag(self) -> int:
        """Get the tag of the element entity."""
        return self.tag_

    def set_element_type(self, element_type: int):
        """Set element type in element entity."""
        self.element_type_ = element_type

    def get_element_type(self) -> int:
        """Get element type in element entity."""
        return self.element_type_

    def set_number_of_elements(self, number_of_elements: int):
        """Set the number of elements in entity."""
        self.number_of_elements_ = number_of_elements

    def get_number_of_elements(self) -> int:
        """Get the number of elements in entity."""
        return self.number_of_elements_

    def add_element(self, element: Element):
        """Add a new element to the entity."""
        self.elements_[element.get_tag()] = element

    def get_element(self, tag: int) -> Element:
        """Get an element from the entity."""
        return self.elements_[tag]

    def get_elements(self) -> List[Element]:
        """Return all the elements of this entity."""
        return self.elements_.values()

    def __str__(self):
        io = StringIO()
        io.write("---- Element entity # %s ----\n" % self.get_tag())
        io.write("Dimension: %s\n" % self.get_dimension())
        io.write("Element type: %s\n" % self.get_element_type())
        io.write("Number of elements: %s\n" % self.get_number_of_elements())
        return io.getvalue()
