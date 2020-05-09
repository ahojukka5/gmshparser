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


def get_triangles(mesh):
    """ Return tuple (X, Y, T) of triangular data.

    Data can be used effectively in matplotlib's `triplot`:

    >>> X, Y, T = get_triangles(mesh)
    >>> plt.triplot(X, Y, T)
    """
    elements = {}
    nodes = {}
    node_ids = set()

    for entity in mesh.get_element_entities():
        eltype = entity.get_element_type()
        if entity.get_dimension() == 2 and eltype == 2:
            for element in entity.get_elements():
                elid = element.get_tag()
                elcon = element.get_connectivity()
                elements[elid] = elcon
                for c in elcon:
                    node_ids.add(c)

    for entity in mesh.get_node_entities():
        for node in entity.get_nodes():
            nid = node.get_tag()
            if nid not in node_ids:
                continue
            ncoords = node.get_coordinates()
            nodes[nid] = ncoords

    invP = {}
    X = []
    Y = []

    for (i, nid) in enumerate(node_ids):
        invP[nid] = i
        X.append(nodes[nid][0])
        Y.append(nodes[nid][1])

    T = []
    for element in elements.values():
        T.append([invP[c] for c in element])

    return X, Y, T
