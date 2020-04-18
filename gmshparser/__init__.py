from typing import List, Tuple, Dict, Type, TextIO


def parse_ints(io: TextIO) -> List[int]:
    """Parse first line of io to list of integers.

    Parameters
    ----------
    io :: TextIO
        Object supporting `readline()`

    Returns
    -------
    integers :: List[int]
        A list of integers

    Examples
    --------
    >>> data = StringIO("1 2 3 4")
    >>> parse_ints(data)
    [1, 2, 3, 4]
    """
    line = io.readline()
    line = line.strip()
    parts = line.split(" ")
    ints = map(int, parts)
    return list(ints)


def parse_floats(io: TextIO) -> List[float]:
    """Parse first line of io to list of floats.

    Parameters
    ----------
    io :: TextIO
        Object supporting `readline()`

    Returns
    -------
    floats :: List[float]
        A list of floats

    Examples
    --------
    >>> data = StringIO("1.1 2.2 3.3 4.4")
    >>> parse_floats(data)
    [1.1, 2.2, 3.3, 4.4]
    """
    line = io.readline()
    line = line.strip()
    parts = line.split(" ")
    ints = map(float, parts)
    return list(ints)


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


class NodeEntity(object):

    """ NodeEntity class holds nodes for one block. """

    def __init__(self):
        self.dimension_ = -1
        self.tag_ = -1
        self.number_of_parametric_coordinates_ = -1
        self.number_of_nodes_ = -1
        self.nodes_ = {}

    def set_dimension(self, dimension: int):
        """Set the dimension of the entity to `dimension`."""
        self.dimension_ = dimension

    def get_dimension(self) -> int:
        """Get the dimension of the entity."""
        return self.dimension_

    def set_tag(self, tag: int):
        """Set the tag of the entity."""
        self.tag_ = tag

    def get_tag(self) -> int:
        """Get the tag of the entity."""
        return self.tag_

    def set_number_of_parametric_coordinates(self, npar: int):
        """Set the number of parametric coordinates of the entity."""
        self.number_of_parametric_coordinates_ = npar

    def get_number_of_parametric_coordinates(self) -> int:
        """Get the number of parametric coordinates of the entity."""
        return self.number_of_parametric_coordinates_

    def set_number_of_nodes(self, number_of_nodes: int):
        """Set the number of nodes of the entity."""
        self.number_of_nodes_ = number_of_nodes

    def get_number_of_nodes(self) -> int:
        """Get the number of nodes of the entity."""
        return self.number_of_nodes_

    def add_node(self, node: Node):
        """Add new node to entity."""
        self.nodes_[node.get_tag()] = node

    def get_node(self, tag: int):
        """Get node from entity by its tag."""
        return self.nodes_[tag]


class Mesh(object):

    """Mesh is the main class of the package."""

    def __init__(self):
        self.version_ = "unknown"
        self.ascii_ = False
        self.precision_ = -1  # t_size
        self.number_of_entities_ = -1
        self.number_of_nodes_ = -1
        self.min_node_tag_ = -1
        self.max_node_tag_ = -1
        self.entities_ = {}

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


class AbstractParser(object):
    def parse(self, mesh: Mesh, io: TextIO) -> None:
        raise NotImplementedError(
            "You have to implement parser(self, mesh, io) to your parser")


class MeshFormatParser(AbstractParser):
    def parse(self, mesh: Mesh, io: TextIO) -> None:
        s = io.readline().strip().split(" ")
        mesh.set_version(float(s[0]))
        mesh.set_ascii(int(s[1]) == 0)
        mesh.set_precision(int(s[2]))


class NodesParser(AbstractParser):

    def parse(self, mesh: Mesh, io: TextIO) -> None:
        meta = parse_ints(io)
        mesh.set_number_of_entities(meta[0])
        mesh.set_number_of_nodes(meta[1])
        mesh.set_min_node_tag(meta[2])
        mesh.set_max_node_tag(meta[3])
        for i in range(mesh.get_number_of_entities()):
            emeta = parse_ints(io)
            entity = NodeEntity()
            entity.set_dimension(emeta[0])
            entity.set_tag(emeta[1])
            entity.set_number_of_parametric_coordinates(emeta[2])
            entity.set_number_of_nodes(emeta[3])
            node_tags = []
            for j in range(entity.get_number_of_nodes()):
                tag = int(io.readline())
                node = Node()
                node.set_tag(tag)
                node_tags.append(tag)
                entity.add_node(node)
            for tag in node_tags:
                coordinates = parse_floats(io)
                node = entity.get_node(tag)
                node.set_coordinates(tuple(coordinates))
            mesh.add_node_entity(entity)


PARSERS = {
    "$MeshFormat": MeshFormatParser,
    "$Nodes": NodesParser
}


def parse_io(io: TextIO, parsers: Dict[str, Type[AbstractParser]]) -> Mesh:
    """Parse input stream using `parsers` and return `Mesh` object. """
    mesh = Mesh()
    for line in io:
        line = line.strip()
        if not line.startswith("$"):
            continue
        if line.startswith("$End"):
            continue
        if line not in parsers:
            continue
        parsers[line]().parse(mesh, io)
    return mesh


def parse(filename: str) -> Mesh:
    """Parse Gmsh .msh file and return `Mesh` object."""
    with open(filename, "r") as fid:
        return parse_io(fid, PARSERS)
