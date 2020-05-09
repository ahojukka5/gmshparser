from gmshparser.nodes_parser import NodesParser
from gmshparser.mesh import Mesh
from io import StringIO

__content__ = """
$Nodes
1 6 1 6
2 1 0 6
1
2
3
4
5
6
0. 0. 0.
1. 0. 0.
1. 1. 0.
0. 1. 0.
2. 0. 0.
2. 1. 0.
$EndNodes
"""


def test_nodes_parser():
    parser = NodesParser()
    mesh = Mesh()
    data = StringIO(__content__.strip())
    parser.parse(mesh, data)

    assert mesh.get_number_of_nodes() == 6
    assert mesh.get_min_node_tag() == 1
    assert mesh.get_max_node_tag() == 6
    assert mesh.has_node_entity(2, 1)

    entity = mesh.get_node_entity(2, 1)
    assert entity.get_tag() == 1
    assert entity.get_dimension() == 2
    assert entity.get_number_of_parametric_coordinates() == 0
    assert entity.get_number_of_nodes() == 6

    assert entity.get_node(1).get_tag() == 1
    assert entity.get_node(1).get_coordinates() == (0.0, 0.0, 0.0)
    assert entity.get_node(2).get_tag() == 2
    assert entity.get_node(2).get_coordinates() == (1.0, 0.0, 0.0)
    assert entity.get_node(3).get_tag() == 3
    assert entity.get_node(3).get_coordinates() == (1.0, 1.0, 0.0)
    assert entity.get_node(4).get_tag() == 4
    assert entity.get_node(4).get_coordinates() == (0.0, 1.0, 0.0)
    assert entity.get_node(5).get_tag() == 5
    assert entity.get_node(5).get_coordinates() == (2.0, 0.0, 0.0)
    assert entity.get_node(6).get_tag() == 6
    assert entity.get_node(6).get_coordinates() == (2.0, 1.0, 0.0)
