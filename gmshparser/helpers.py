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
    """Return tuple (X, Y, T) of triangular data.

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

    for i, nid in enumerate(node_ids):
        invP[nid] = i
        X.append(nodes[nid][0])
        Y.append(nodes[nid][1])

    T = []
    for element in elements.values():
        T.append([invP[c] for c in element])

    return X, Y, T


def get_quads(mesh):
    """Return tuple (X, Y, Q) of quadrilateral data.

    Extracts 4-node quadrilateral elements (element type 3) from mesh.
    Data can be used with matplotlib's patches:

    >>> X, Y, Q = get_quads(mesh)
    >>> import matplotlib.pyplot as plt
    >>> import matplotlib.patches as patches
    >>> fig, ax = plt.subplots()
    >>> for quad in Q:
    >>>     coords = [[X[i], Y[i]] for i in quad]
    >>>     polygon = patches.Polygon(coords, fill=False, edgecolor='black')
    >>>     ax.add_patch(polygon)

    Parameters
    ----------
    mesh : Mesh
        Mesh object containing quadrilateral elements

    Returns
    -------
    X : list
        List of x-coordinates of nodes
    Y : list
        List of y-coordinates of nodes
    Q : list
        List of quadrilateral connectivity, each entry is [n0, n1, n2, n3]
    """
    elements = {}
    nodes = {}
    node_ids = set()

    for entity in mesh.get_element_entities():
        eltype = entity.get_element_type()
        if entity.get_dimension() == 2 and eltype == 3:
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

    for i, nid in enumerate(sorted(node_ids)):
        invP[nid] = i
        X.append(nodes[nid][0])
        Y.append(nodes[nid][1])

    Q = []
    for element in elements.values():
        Q.append([invP[c] for c in element])

    return X, Y, Q


def get_elements_2d(mesh):
    """Return 2D mesh elements (triangles and quads) for visualization.

    Extracts all 2D elements from the mesh, supporting both triangular
    (type 2) and quadrilateral (type 3) elements.

    Parameters
    ----------
    mesh : Mesh
        Mesh object containing 2D elements

    Returns
    -------
    dict
        Dictionary with keys:
        - 'nodes': dict mapping node_id to (x, y) coordinates
        - 'triangles': list of triangle connectivity [n0, n1, n2]
        - 'quads': list of quad connectivity [n0, n1, n2, n3]
        - 'node_ids': list of all node IDs used
    """
    triangles = []
    quads = []
    nodes = {}
    node_ids = set()

    # Extract elements
    for entity in mesh.get_element_entities():
        eltype = entity.get_element_type()
        if entity.get_dimension() == 2:
            for element in entity.get_elements():
                elcon = element.get_connectivity()
                for c in elcon:
                    node_ids.add(c)

                if eltype == 2:  # Triangle
                    triangles.append(elcon)
                elif eltype == 3:  # Quad
                    quads.append(elcon)

    # Extract node coordinates
    for entity in mesh.get_node_entities():
        for node in entity.get_nodes():
            nid = node.get_tag()
            if nid in node_ids:
                ncoords = node.get_coordinates()
                nodes[nid] = (ncoords[0], ncoords[1])

    return {
        "nodes": nodes,
        "triangles": triangles,
        "quads": quads,
        "node_ids": sorted(node_ids),
    }
