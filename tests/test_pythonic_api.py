from dataclasses import FrozenInstanceError
from io import StringIO

import pytest

import gmshparser
from gmshparser.api import ElementType, Mesh as ModernMesh, Version

MESH = """$MeshFormat
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
0.0 0.0 0.0
1.0 0.0 0.0
1.0 1.0 0.0
0.0 1.0 0.0
2.0 0.0 0.0
2.0 1.0 0.0
$EndNodes
$Elements
1 2 1 2
2 1 3 2
1 1 2 3 4
2 2 5 6 3
$EndElements
"""

PARAMETRIC_MESH = """$MeshFormat
4.1 0 8
$EndMeshFormat
$Nodes
1 1 1 1
2 1 1 1
1
0.0 0.0 0.0 0.25 0.75
$EndNodes
$Elements
0 0 0 0
$EndElements
"""


def test_read_stream_exposes_flat_pythonic_collections():
    mesh = gmshparser.read(StringIO(MESH), name="memory.msh")

    assert isinstance(mesh, ModernMesh)
    assert mesh.version == Version(4, 1)
    assert str(mesh.version) == "4.1"
    assert float(mesh.version) == 4.1
    assert mesh.is_ascii is True
    assert mesh.data_size == 8
    assert mesh.dimension == 2

    assert len(mesh.nodes) == 6
    assert mesh.nodes.tags == (1, 2, 3, 4, 5, 6)
    assert 1 in mesh.nodes
    assert mesh.nodes.get(999) is None
    assert mesh.nodes[2].coordinates == (1.0, 0.0, 0.0)
    assert (mesh.nodes[2].x, mesh.nodes[2].y, mesh.nodes[2].z) == (
        1.0,
        0.0,
        0.0,
    )
    assert tuple(mesh.nodes[2]) == (1.0, 0.0, 0.0)
    assert mesh.nodes[2].entity_key == (2, 1)

    assert len(mesh.elements) == 2
    assert mesh.elements.tags == (1, 2)
    assert mesh.elements.types == frozenset({ElementType.QUADRANGLE})
    element = mesh.elements[1]
    assert element.type is ElementType.QUADRANGLE
    assert element.element_type is ElementType.QUADRANGLE
    assert element.type_id == 3
    assert element.node_tags == (1, 2, 3, 4)
    assert element.connectivity == (1, 2, 3, 4)
    assert tuple(node.tag for node in element) == (1, 2, 3, 4)
    assert element.nodes[0] is mesh.nodes[1]
    assert element.entity_key == (2, 1)
    assert len(element) == 4


def test_filtering_and_unified_entity_access_share_value_objects():
    mesh = gmshparser.read(StringIO(MESH))

    surface_nodes = mesh.nodes.where(entity=(2, 1))
    quads = mesh.elements.where(
        element_type=ElementType.QUADRANGLE,
        entity=(2, 1),
    )

    assert surface_nodes.tags == (1, 2, 3, 4, 5, 6)
    assert quads.tags == (1, 2)
    assert mesh.elements.by_type(3) == quads

    entity = mesh.entities[(2, 1)]
    assert entity.key == (2, 1)
    assert len(entity.nodes) == 6
    assert len(entity.elements) == 2
    assert entity.nodes[1] is mesh.nodes[1]
    assert entity.elements[1] is mesh.elements[1]
    assert entity.element_types == frozenset({ElementType.QUADRANGLE})
    assert mesh.entities.where(dimension=2).keys == ((2, 1),)
    assert mesh.entities.where(element_type=3).keys == ((2, 1),)


def test_nodes_and_mesh_values_are_immutable():
    mesh = gmshparser.read(StringIO(MESH))

    with pytest.raises(FrozenInstanceError):
        mesh.nodes[1].tag = 99

    with pytest.raises(FrozenInstanceError):
        mesh.name = "other.msh"


def test_parametric_coordinates_are_separated_from_cartesian_coordinates():
    mesh = gmshparser.read(StringIO(PARAMETRIC_MESH))
    node = mesh.nodes[1]

    assert node.coordinates == (0.0, 0.0, 0.0)
    assert node.parametric_coordinates == (0.25, 0.75)
    assert node.is_parametric is True
    assert mesh.entities[(2, 1)].has_parametric_nodes is True


def test_element_type_accepts_unnamed_gmsh_values():
    element_type = ElementType(92)

    assert int(element_type) == 92
    assert element_type.name == "TYPE_92"


def test_mesh_bounds_are_computed_from_nodes():
    mesh = gmshparser.read(StringIO(MESH))

    assert mesh.bounds == ((0.0, 0.0, 0.0), (2.0, 1.0, 0.0))


def test_helpers_accept_the_modern_api():
    mesh = gmshparser.read(StringIO(MESH))

    x_coordinates, y_coordinates, quads = gmshparser.helpers.get_quads(mesh)
    mixed = gmshparser.helpers.get_elements_2d(mesh)

    assert x_coordinates == [0.0, 1.0, 1.0, 0.0, 2.0, 2.0]
    assert y_coordinates == [0.0, 0.0, 1.0, 1.0, 0.0, 1.0]
    assert quads == [[0, 1, 2, 3], [1, 4, 5, 2]]
    assert mixed["quads"] == [[1, 2, 3, 4], [2, 5, 6, 3]]


def test_read_path_and_parse_keep_both_apis(tmp_path):
    path = tmp_path / "mesh.msh"
    path.write_text(MESH)

    modern = gmshparser.read(path)
    legacy = gmshparser.parse(str(path))

    assert isinstance(modern, ModernMesh)
    assert modern.name == str(path)
    assert isinstance(legacy, gmshparser.Mesh)
    assert legacy.get_number_of_nodes() == len(modern.nodes)
    assert legacy.get_number_of_elements() == len(modern.elements)
