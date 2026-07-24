from io import StringIO

import numpy as np
import pytest

import gmshparser
import gmshparser.numpy as gnp
from gmshparser import ElementType

MIXED_MESH = """$MeshFormat
4.1 0 8
$EndMeshFormat
$Nodes
1 4 10 40
2 1 0 4
10
20
30
40
0.0 0.0 0.0
1.0 0.0 0.0
0.0 1.0 0.0
1.0 1.0 0.0
$EndNodes
$Elements
2 2 100 200
1 1 1 1
100 10 20
2 1 2 1
200 10 20 30
$EndElements
"""

EMPTY_MESH = """$MeshFormat
4.1 0 8
$EndMeshFormat
$Nodes
0 0 0 0
$EndNodes
$Elements
0 0 0 0
$EndElements
"""


def test_to_numpy_preserves_tags_and_groups_rectangular_cell_blocks():
    mesh = gmshparser.read(StringIO(MIXED_MESH))

    arrays = gnp.to_numpy(mesh)

    np.testing.assert_array_equal(
        arrays.points,
        np.asarray(
            [
                [0.0, 0.0, 0.0],
                [1.0, 0.0, 0.0],
                [0.0, 1.0, 0.0],
                [1.0, 1.0, 0.0],
            ]
        ),
    )
    np.testing.assert_array_equal(arrays.node_tags, [10, 20, 30, 40])
    np.testing.assert_array_equal(
        arrays.node_entity_keys,
        [[2, 1], [2, 1], [2, 1], [2, 1]],
    )
    assert arrays.element_types == (ElementType.LINE, ElementType.TRIANGLE)
    assert arrays.number_of_nodes == 4
    assert arrays.number_of_elements == 2

    line = arrays.cells[ElementType.LINE]
    triangle = arrays.cell_block(2)

    np.testing.assert_array_equal(line.connectivity, [[0, 1]])
    np.testing.assert_array_equal(line.element_tags, [100])
    np.testing.assert_array_equal(line.entity_keys, [[1, 1]])
    assert line.number_of_elements == 1
    assert line.nodes_per_element == 2

    np.testing.assert_array_equal(triangle.connectivity, [[0, 1, 2]])
    np.testing.assert_array_equal(triangle.element_tags, [200])
    np.testing.assert_array_equal(triangle.entity_keys, [[2, 1]])
    np.testing.assert_array_equal(arrays.cell_node_tags(2), [[10, 20, 30]])


def test_to_numpy_can_filter_element_types_without_reindexing_nodes():
    mesh = gmshparser.read(StringIO(MIXED_MESH))

    arrays = gnp.to_numpy(mesh, element_types=ElementType.TRIANGLE)

    assert arrays.element_types == (ElementType.TRIANGLE,)
    assert arrays.number_of_nodes == 4
    assert arrays.number_of_elements == 1
    np.testing.assert_array_equal(
        arrays.cells[ElementType.TRIANGLE].connectivity,
        [[0, 1, 2]],
    )


def test_to_numpy_accepts_custom_coordinate_and_integer_dtypes():
    mesh = gmshparser.read(StringIO(MIXED_MESH))

    arrays = gnp.to_numpy(
        mesh,
        coordinate_dtype=np.float32,
        index_dtype=np.int32,
    )

    assert arrays.points.dtype == np.dtype(np.float32)
    assert arrays.node_tags.dtype == np.dtype(np.int32)
    assert arrays.node_entity_keys.dtype == np.dtype(np.int32)
    assert arrays.cells[ElementType.LINE].connectivity.dtype == np.dtype(np.int32)


def test_numpy_arrays_are_detached_from_the_immutable_mesh():
    mesh = gmshparser.read(StringIO(MIXED_MESH))
    arrays = gnp.to_numpy(mesh)

    arrays.points[0, 0] = 99.0

    assert mesh.nodes[10].x == 0.0
    assert arrays.points[0, 0] == 99.0


def test_cell_mapping_is_read_only_but_arrays_are_writable():
    mesh = gmshparser.read(StringIO(MIXED_MESH))
    arrays = gnp.to_numpy(mesh)

    with pytest.raises(TypeError):
        arrays.cells[ElementType.QUADRANGLE] = arrays.cells[ElementType.LINE]

    arrays.cells[ElementType.LINE].connectivity[0, 0] = 1
    assert arrays.cells[ElementType.LINE].connectivity[0, 0] == 1


def test_to_numpy_rejects_non_integer_index_dtype():
    mesh = gmshparser.read(StringIO(MIXED_MESH))

    with pytest.raises(TypeError, match="index_dtype must be an integer"):
        gnp.to_numpy(mesh, index_dtype=np.float64)


def test_to_numpy_requires_the_modern_mesh_model(tmp_path):
    path = tmp_path / "mesh.msh"
    path.write_text(MIXED_MESH)
    legacy = gmshparser.parse(str(path))

    with pytest.raises(TypeError, match="gmshparser.read"):
        gnp.to_numpy(legacy)


def test_empty_mesh_produces_stable_empty_shapes():
    arrays = gnp.to_numpy(gmshparser.read(StringIO(EMPTY_MESH)))

    assert arrays.points.shape == (0, 3)
    assert arrays.node_tags.shape == (0,)
    assert arrays.node_entity_keys.shape == (0, 2)
    assert arrays.element_types == ()
    assert arrays.number_of_nodes == 0
    assert arrays.number_of_elements == 0
