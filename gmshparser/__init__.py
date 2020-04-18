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

    def __init__(self):
        self.version = None
        self.ascii = None
        self.size = None

    def set_format(self, version, ascii, size):
        self.version = version
        self.ascii = ascii
        self.size = size


class AbstractParser(object):
    def parse(self, mesh, io):
        raise NotImplementedError(
            "You have to implement parser(self, mesh, io) to your parser")


class MeshFormatParser(AbstractParser):
    def parse(self, mesh, io):
        s = io.readline().split(" ")
        mesh.set_format(float(s[0]), int(s[1]), int(s[2]))


class NodesParser(AbstractParser):
    def parse(self, mesh, io):
        s = io.readline().split(" ")
        number_of_entities = int(s[0])
        number_of_nodes = int(s[1])
        node_min_label = int(s[2])
        node_max_label = int(s[3])


PARSERS = {
    "$MeshFormat": MeshFormatParser,
    "$Nodes": NodesParser,
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
