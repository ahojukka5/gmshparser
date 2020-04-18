from typing import List, TextIO

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

class Mesh(object):

    """ Mesh is the main object of the package, containing the Gmsh .msh information. """

    def __init__(self):
        self.version_ = "unknown"
        self.ascii_ = False
        self.precision_ = -1 # t_size

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




class AbstractParser(object):
    def parse(self, mesh, io):
        raise NotImplementedError(
            "You have to implement parser(self, mesh, io) to your parser")


class MeshFormatParser(AbstractParser):
    def parse(self, mesh, io):
        s = io.readline().strip().split(" ")
        mesh.set_version(float(s[0]))
        mesh.set_ascii(int(s[1]) == 0)
        mesh.set_precision(int(s[2]))


class NodesParser(AbstractParser):
    def parse(self, mesh, io):
        s = io.readline().split(" ")
        number_of_entities = int(s[0])
        number_of_nodes = int(s[1])
        node_min_label = int(s[2])
        node_max_label = int(s[3])


PARSERS = {
    "$MeshFormat": MeshFormatParser,
}

def parse_io(io, parsers=PARSERS):
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
