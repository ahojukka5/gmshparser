from io import StringIO

from gmshparser.element_entity import ElementEntity
from gmshparser.node_entity import NodeEntity


class Mesh:
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
        self.physical_names_ = {}
        self.entity_physical_tags_ = {}
        self.element_physical_tags_ = {}

    def set_name(self, name: str):
        """Set the name of the mesh."""
        self.name_ = name

    def get_name(self) -> str:
        """Get the name of the mesh."""
        return self.name_

    def set_version(self, version: float):
        """Set the version of the Mesh object"""
        self.version_ = version
        major = int(version)
        minor = int(round((version - major) * 10))
        self.version_major_ = major
        self.version_minor_ = minor

    def get_version(self) -> float | None:
        """Get the version of the Mesh object"""
        return self.version_

    def get_version_major(self) -> int | None:
        """Get the major version number."""
        return self.version_major_

    def get_version_minor(self) -> int | None:
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

    def get_node_entities(self) -> list[NodeEntity]:
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

    def get_element_entities(self) -> list[ElementEntity]:
        """Get all element entities as dictionary."""
        return self.element_entities_.values()

    def set_physical_name(self, dimension: int, tag: int, name: str):
        """Store a physical group name without changing the legacy object model."""
        self.physical_names_[(dimension, tag)] = name

    def get_physical_name(self, dimension: int, tag: int) -> str | None:
        """Return a physical group name when one was declared."""
        return self.physical_names_.get((dimension, tag))

    def get_physical_names(self) -> dict[tuple[int, int], str]:
        """Return declared physical group names keyed by ``(dimension, tag)``."""
        return dict(self.physical_names_)

    def set_entity_physical_tags(self, dimension: int, tag: int, physical_tags):
        """Replace physical tags assigned to one elementary entity."""
        self.entity_physical_tags_[(dimension, tag)] = self._normalize_tags(
            physical_tags
        )

    def add_entity_physical_tags(self, dimension: int, tag: int, physical_tags):
        """Add physical tags assigned to one elementary entity."""
        existing = self.entity_physical_tags_.get((dimension, tag), ())
        self.entity_physical_tags_[(dimension, tag)] = self._normalize_tags(
            (*existing, *physical_tags)
        )

    def get_entity_physical_tags(self, dimension: int, tag: int) -> tuple[int, ...]:
        """Return physical tags assigned to one elementary entity."""
        return self.entity_physical_tags_.get((dimension, tag), ())

    def set_element_physical_tags(self, element_tag: int, physical_tags):
        """Store physical tags carried directly by one legacy element record."""
        self.element_physical_tags_[element_tag] = self._normalize_tags(physical_tags)

    def get_element_physical_tags(self, element_tag: int) -> tuple[int, ...]:
        """Return physical tags carried directly by one element."""
        return self.element_physical_tags_.get(element_tag, ())

    @staticmethod
    def _normalize_tags(tags) -> tuple[int, ...]:
        normalized = []
        for tag in tags:
            value = int(tag)
            if value > 0 and value not in normalized:
                normalized.append(value)
        return tuple(normalized)

    def __str__(self):
        io = StringIO()
        io.write(f"Mesh name: {self.get_name()}\n")
        io.write(f"Mesh version: {self.get_version()}\n")
        io.write(f"Number of nodes: {self.get_number_of_nodes()}\n")
        io.write(f"Minimum node tag: {self.get_min_node_tag()}\n")
        io.write(f"Maximum node tag: {self.get_max_node_tag()}\n")
        nnent = self.get_number_of_node_entities()
        io.write(f"Number of node entities: {nnent}\n")
        io.write(f"Number of elements: {self.get_number_of_elements()}\n")
        io.write(f"Minimum element tag: {self.get_min_element_tag()}\n")
        io.write(f"Maximum element tag: {self.get_max_element_tag()}\n")
        neent = self.get_number_of_element_entities()
        io.write(f"Number of element entities: {neent}")
        return io.getvalue()
