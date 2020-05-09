import io
from gmshparser.mesh import Mesh
from gmshparser.node import Node
from gmshparser.node_entity import NodeEntity
from gmshparser.element import Element
from gmshparser.element_entity import ElementEntity
from gmshparser.helpers import parse_ints, parse_floats, get_triangles


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
