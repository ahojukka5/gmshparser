from gmshparser.node_entity import NodeEntity


class Mesh(object):

    """Mesh is the main class of the package."""

    def __init__(self):
        self.name_ = "newmesh"
        self.version_ = "unknown"
        self.ascii_ = False
        self.precision_ = -1  # t_size
        self.number_of_entities_ = -1
        self.number_of_nodes_ = -1
        self.min_node_tag_ = -1
        self.max_node_tag_ = -1
        self.entities_ = {}

    def set_name(self, name: str):
        """Set the name of the mesh."""
        self.name_ = name

    def get_name(self) -> str:
        """Get the name of the mesh."""
        return self.name_

    def set_version(self, version: str):
        """Set the version of the Mesh object"""
        self.version_ = version

    def get_version(self) -> str:
        """Get the version of the Mesh object"""
        return self.version_

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

    def set_number_of_entities(self, number_of_entities: int):
        """Set number of entities."""
        self.number_of_entities_ = number_of_entities

    def get_number_of_entities(self) -> int:
        """Get number of entities."""
        return self.number_of_entities_

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

    def has_node_entity(self, entity_tag) -> bool:
        """Test does mesh have entity with `entity_tag`."""
        return entity_tag in self.entities_

    def add_node_entity(self, entity: NodeEntity):
        """Add node entity to mesh."""
        self.entities_[entity.get_tag()] = entity

    def get_node_entity(self, tag: int):
        """Get node entity based on tag."""
        return self.entities_[tag]
