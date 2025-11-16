from typing import List, Optional
from gmshparser.node_entity import NodeEntity
from gmshparser.element_entity import ElementEntity
from io import StringIO


class Mesh(object):
    """Mesh is the main class of the package."""

    def __init__(self):
        self.name_ = "New Mesh"
        self.version_ = None  # Will be set when parsing MeshFormat
        self.version_major_ = None
        self.version_minor_ = None
        self.ascii_ = True
        self.precision_ = 8  # t_size
        self.number_of_node_entities_ = 0
        self.number_of_nodes_ = 0
        self.min_node_tag_ = 0
        self.max_node_tag_ = 0
        self.node_entities_ = {}
        self.number_of_element_entities_ = 0
        self.number_of_elements_ = 0
        self.min_element_tag_ = 0
        self.max_element_tag_ = 0
        self.element_entities_ = {}

    def set_name(self, name: str):
        """Set the name of the mesh."""
        self.name_ = name

    def get_name(self) -> str:
        """Get the name of the mesh."""
        return self.name_

    def set_version(self, version: float):
        """Set the version of the Mesh object"""
        self.version_ = version
        # Parse major and minor version numbers
        major = int(version)
        minor = int(round((version - major) * 10))
        self.version_major_ = major
        self.version_minor_ = minor

    def get_version(self) -> Optional[float]:
        """Get the version of the Mesh object"""
        return self.version_

    def get_version_major(self) -> Optional[int]:
        """Get the major version number."""
        return self.version_major_

    def get_version_minor(self) -> Optional[int]:
        """Get the minor version number."""
        return self.version_minor_

    def set_ascii(self, is_ascii: bool):
        """Set a boolean flag whether this mesh is ASCII or binary"""
        self.ascii_ = is_ascii

    def get_ascii(self) -> bool:
        """Get a boolean flag whether this mesh is ASCII of binary"""
        return self.ascii_

    def set_precision(self, precision: int):
        """Set the precision of the mesh (8)"""
        self.precision_ = precision

    def get_precision(self) -> int:
        """Get the precision of the mesh"""
        return self.precision_

    def set_number_of_node_entities(self, number_of_node_entities: int):
        """Set number of node entities."""
        self.number_of_node_entities_ = number_of_node_entities

    def get_number_of_node_entities(self) -> int:
        """Get number of node entities."""
        return self.number_of_node_entities_

    def set_number_of_nodes(self, number_of_nodes: int):
        """Set number of nodes."""
        self.number_of_nodes_ = number_of_nodes

    def get_number_of_nodes(self) -> int:
        """Get number of nodes."""
        return self.number_of_nodes_

    def set_min_node_tag(self, min_node_tag: int):
        """Set node minimum tag."""
        self.min_node_tag_ = min_node_tag

    def get_min_node_tag(self) -> int:
        """Get node minimum tag."""
        return self.min_node_tag_

    def set_max_node_tag(self, max_node_tag: int):
        """Set node maximum tag."""
        self.max_node_tag_ = max_node_tag

    def get_max_node_tag(self) -> int:
        """Get node maximum tag."""
        return self.max_node_tag_

    def has_node_entity(self, dim: int, tag: int) -> bool:
        """Test does mesh have node entity of dimension `dim` and tag `tag`."""
        return (dim, tag) in self.node_entities_

    def add_node_entity(self, node_entity: NodeEntity):
        """Add node entity to mesh."""
        dim = node_entity.get_dimension()
        tag = node_entity.get_tag()
        self.node_entities_[(dim, tag)] = node_entity

    def get_node_entity(self, dim: int, tag: int):
        """Get node entity based on dimension and tag."""
        return self.node_entities_[(dim, tag)]

    def get_node_entities(self) -> List[NodeEntity]:
        """Get all node entities of mesh."""
        return self.node_entities_.values()

    def set_number_of_element_entities(self, number_of_element_entities: int):
        """Set number of element entities."""
        self.number_of_element_entities_ = number_of_element_entities

    def get_number_of_element_entities(self) -> int:
        """Get number of element entities."""
        return self.number_of_element_entities_

    def set_number_of_elements(self, number_of_elements: int):
        """Set number of elements."""
        self.number_of_elements_ = number_of_elements

    def get_number_of_elements(self) -> int:
        """Get number of elements."""
        return self.number_of_elements_

    def set_min_element_tag(self, min_element_tag: int):
        """Set element minimum tag."""
        self.min_element_tag_ = min_element_tag

    def get_min_element_tag(self) -> int:
        """Get element minimum tag."""
        return self.min_element_tag_

    def set_max_element_tag(self, max_element_tag: int):
        """Set element maximum tag."""
        self.max_element_tag_ = max_element_tag

    def get_max_element_tag(self) -> int:
        """Get element maximum tag."""
        return self.max_element_tag_

    def has_element_entity(self, dim: int, tag: int) -> bool:
        """Test does mesh have element entity with `(dim, tag)`."""
        return (dim, tag) in self.element_entities_

    def add_element_entity(self, element_entity: ElementEntity):
        """Add element entity to mesh."""
        dim = element_entity.get_dimension()
        tag = element_entity.get_tag()
        self.element_entities_[(dim, tag)] = element_entity

    def get_element_entity(self, dim: int, tag: int) -> ElementEntity:
        """Get element entity based on dimension `dim` and tag `tag`."""
        return self.element_entities_[(dim, tag)]

    def get_element_entities(self) -> List[ElementEntity]:
        """Get all element entities as dictionary."""
        return self.element_entities_.values()

    def __str__(self):
        io = StringIO()
        io.write("Mesh name: %s\n" % self.get_name())
        io.write("Mesh version: %s\n" % self.get_version())
        io.write("Number of nodes: %s\n" % self.get_number_of_nodes())
        io.write("Minimum node tag: %s\n" % self.get_min_node_tag())
        io.write("Maximum node tag: %s\n" % self.get_max_node_tag())
        nnent = self.get_number_of_node_entities()
        io.write("Number of node entities: %s\n" % nnent)
        io.write("Number of elements: %s\n" % self.get_number_of_elements())
        io.write("Minimum element tag: %s\n" % self.get_min_element_tag())
        io.write("Maximum element tag: %s\n" % self.get_max_element_tag())
        neent = self.get_number_of_element_entities()
        io.write("Number of element entities: %s" % neent)
        return io.getvalue()
