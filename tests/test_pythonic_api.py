from io import StringIO

import gmshparser
from gmshparser.api import Mesh as ModernMesh

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


def test_read_stream_exposes_flat_pythonic_collections():
    mesh = gmshparser.read(StringIO(MESH), name="memory.msh")

    assert isinstance(mesh, ModernMesh)
    assert repr(mesh) == "Mesh(name='memory.msh', version=4.1, nodes=6, elements=2)"
    assert mesh.version == 4.1
    assert mesh.version_info == (4, 1)
    assert mesh.is_ascii is True
    assert mesh.precision == 8

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

    assert len(mesh.elements) == 2
    assert mesh.elements.tags == (1, 2)
    assert mesh.elements.types == frozenset({3})
    assert mesh.elements[1].node_tags == (1, 2, 3, 4)
    assert mesh.elements[1].connectivity == (1, 2, 3, 4)
    assert tuple(mesh.elements[1]) == (1, 2, 3, 4)
    assert len(mesh.elements[1]) == 4


def test_filtering_and_entity_access_share_value_objects():
    mesh = gmshparser.read(StringIO(MESH))

    surface_nodes = mesh.nodes.where(dimension=2, entity_tag=1)
    quads = mesh.elements.where(
        element_type=3,
        dimension=2,
        entity_tag=1,
    )

    assert surface_nodes.tags == (1, 2, 3, 4, 5, 6)
    assert quads.tags == (1, 2)
    assert mesh.elements.by_type(3) == quads

    node_entity = mesh.node_entities[(2, 1)]
    element_entity = mesh.element_entities[(2, 1)]
    assert len(node_entity) == 6
    assert len(element_entity) == 2
    assert node_entity.nodes[1] is mesh.nodes[1]
    assert element_entity.elements[1] is mesh.elements[1]
    assert mesh.node_entities.where(dimension=2).keys == ((2, 1),)


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
