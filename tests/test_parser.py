import gmshparser
import io
import pytest


@pytest.fixture
def mesh():
    data = """
    $MeshFormat
    4.1 0 8
    $EndMeshFormat
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
    $Elements
    1 2 1 2
    2 1 3 2
    1 1 2 3 4
    2 2 5 6 3
    $EndElements
    $NodeData
    1
    "A scalar view"
    1
    0.0
    3
    0
    1
    6
    1 0.0
    2 0.1
    3 0.2
    4 0.0
    5 0.2
    6 0.4
    $EndNodeData
    """
    return gmshparser.parse_io(io.StringIO(data), gmshparser.PARSERS)


def test_abstract_parser(mesh):
    p = gmshparser.AbstractParser()
    with pytest.raises(NotImplementedError):
        p.parse(1, 2)


def test_version(mesh):
    assert mesh.get_version() == 4.1
    assert mesh.get_ascii()
    assert mesh.get_precision() == 8


def test_nodes(mesh):
    assert mesh.get_number_of_nodes() == 6
    assert mesh.get_min_node_tag() == 1
    assert mesh.get_max_node_tag() == 6

    assert mesh.has_node_entity(1)
    entity = mesh.get_node_entity(1)
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
