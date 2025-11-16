import io
from gmshparser.mesh import Mesh
from gmshparser.node import Node
from gmshparser.node_entity import NodeEntity
from gmshparser.element import Element
from gmshparser.element_entity import ElementEntity
from gmshparser.helpers import (
    parse_ints,
    parse_floats,
    get_triangles,
    get_quads,
    get_elements_2d,
)


def test_parse_ints():
    s = io.StringIO("1 2 3 4")
    assert parse_ints(s) == [1, 2, 3, 4]


def test_parse_floats():
    s = io.StringIO("1.1 2.2 3.3 4.4")
    assert parse_floats(s) == [1.1, 2.2, 3.3, 4.4]


def test_get_triangles():
    mesh = Mesh()

    n1 = Node()
    n1.set_tag(1)
    n1.set_coordinates((0.0, 0.0, 0.0))

    n2 = Node()
    n2.set_tag(2)
    n2.set_coordinates((1.0, 0.0, 0.0))

    n3 = Node()
    n3.set_tag(3)
    n3.set_coordinates((0.0, 1.0, 0.0))

    n4 = Node()
    n4.set_tag(4)
    n4.set_coordinates((1.0, 2.0, 3.0))

    ne1 = NodeEntity()
    ne1.set_dimension(2)
    ne1.set_tag(1)
    ne1.add_node(n1)
    ne1.add_node(n2)
    ne1.add_node(n3)
    ne1.add_node(n4)

    e1 = Element()
    e1.set_tag(1)
    e1.set_connectivity([1, 2, 3])

    ee1 = ElementEntity()
    ee1.set_dimension(2)
    ee1.set_tag(1)
    ee1.set_element_type(2)
    ee1.add_element(e1)

    ee2 = ElementEntity()
    ee2.set_dimension(1)
    ee2.set_element_type(3)

    mesh.add_node_entity(ne1)
    mesh.add_element_entity(ee1)
    mesh.add_element_entity(ee2)

    (X, Y, T) = get_triangles(mesh)
    assert X == [0.0, 1.0, 0.0]
    assert Y == [0.0, 0.0, 1.0]
    assert T == [[0, 1, 2]]


def test_get_quads():
    """Test extracting quad elements from mesh."""
    mesh = Mesh()

    # Create 6 nodes for 2 quads
    nodes = []
    coords = [
        (0.0, 0.0, 0.0),
        (1.0, 0.0, 0.0),
        (1.0, 1.0, 0.0),
        (0.0, 1.0, 0.0),
        (2.0, 0.0, 0.0),
        (2.0, 1.0, 0.0),
    ]

    for i, (x, y, z) in enumerate(coords, start=1):
        n = Node()
        n.set_tag(i)
        n.set_coordinates((x, y, z))
        nodes.append(n)

    ne = NodeEntity()
    ne.set_dimension(2)
    ne.set_tag(1)
    for n in nodes:
        ne.add_node(n)

    # Create 2 quad elements
    e1 = Element()
    e1.set_tag(1)
    e1.set_connectivity([1, 2, 3, 4])

    e2 = Element()
    e2.set_tag(2)
    e2.set_connectivity([2, 5, 6, 3])

    ee = ElementEntity()
    ee.set_dimension(2)
    ee.set_tag(1)
    ee.set_element_type(3)  # Quad type
    ee.add_element(e1)
    ee.add_element(e2)

    mesh.add_node_entity(ne)
    mesh.add_element_entity(ee)

    (X, Y, Q) = get_quads(mesh)

    # Check we have 6 nodes
    assert len(X) == 6
    assert len(Y) == 6

    # Check we have 2 quads
    assert len(Q) == 2

    # Check quad connectivity (should have 4 nodes each)
    assert len(Q[0]) == 4
    assert len(Q[1]) == 4


def test_get_elements_2d():
    """Test extracting mixed 2D elements (triangles and quads)."""
    mesh = Mesh()

    # Create 7 nodes
    coords = [
        (0.0, 0.0, 0.0),  # 1
        (1.0, 0.0, 0.0),  # 2
        (0.5, 1.0, 0.0),  # 3
        (2.0, 0.0, 0.0),  # 4
        (3.0, 0.0, 0.0),  # 5
        (3.0, 1.0, 0.0),  # 6
        (2.0, 1.0, 0.0),  # 7
    ]

    nodes = []
    for i, (x, y, z) in enumerate(coords, start=1):
        n = Node()
        n.set_tag(i)
        n.set_coordinates((x, y, z))
        nodes.append(n)

    ne = NodeEntity()
    ne.set_dimension(2)
    ne.set_tag(1)
    for n in nodes:
        ne.add_node(n)

    # Create 1 triangle element
    e_tri = Element()
    e_tri.set_tag(1)
    e_tri.set_connectivity([1, 2, 3])

    ee_tri = ElementEntity()
    ee_tri.set_dimension(2)
    ee_tri.set_tag(1)
    ee_tri.set_element_type(2)  # Triangle
    ee_tri.add_element(e_tri)

    # Create 1 quad element
    e_quad = Element()
    e_quad.set_tag(2)
    e_quad.set_connectivity([4, 5, 6, 7])

    ee_quad = ElementEntity()
    ee_quad.set_dimension(2)
    ee_quad.set_tag(2)
    ee_quad.set_element_type(3)  # Quad
    ee_quad.add_element(e_quad)

    mesh.add_node_entity(ne)
    mesh.add_element_entity(ee_tri)
    mesh.add_element_entity(ee_quad)

    data = get_elements_2d(mesh)

    # Check structure
    assert "nodes" in data
    assert "triangles" in data
    assert "quads" in data
    assert "node_ids" in data

    # Check we have 7 nodes
    assert len(data["nodes"]) == 7

    # Check we have 1 triangle and 1 quad
    assert len(data["triangles"]) == 1
    assert len(data["quads"]) == 1

    # Check triangle has 3 nodes
    assert len(data["triangles"][0]) == 3

    # Check quad has 4 nodes
    assert len(data["quads"][0]) == 4
