import pytest

import gmshparser
import gmshparser.numpy as gnp
from gmshparser import ElementType

MSH_1_MIXED = """$NOD
5
1 0.0 0.0 0.0
2 1.0 0.0 0.0
3 0.0 1.0 0.0
4 1.0 1.0 0.0
5 2.0 1.0 0.0
$ENDNOD
$ELM
2
1 2 99 1 3 1 2 3
2 3 99 1 4 1 2 4 5
$ENDELM
"""

MSH_2_MIXED = """$MeshFormat
2.2 0 8
$EndMeshFormat
$Nodes
5
1 0.0 0.0 0.0
2 1.0 0.0 0.0
3 0.0 1.0 0.0
4 1.0 1.0 0.0
5 2.0 1.0 0.0
$EndNodes
$Elements
2
1 2 2 99 1 1 2 3
2 3 2 99 1 1 2 4 5
$EndElements
"""


@pytest.mark.parametrize(
    ("filename", "content"),
    [
        ("mixed-v1.msh", MSH_1_MIXED),
        ("mixed-v2.msh", MSH_2_MIXED),
    ],
)
def test_flat_formats_preserve_multiple_element_types_on_one_entity(
    tmp_path,
    filename,
    content,
):
    path = tmp_path / filename
    path.write_text(content)

    legacy = gmshparser.parse(str(path))

    assert legacy.get_number_of_elements() == 2
    assert legacy.get_number_of_element_entities() == 2
    assert len(tuple(legacy.get_element_entities())) == 2
    assert legacy.has_element_entity(2, 1)
    assert legacy.has_element_entity(2, 1, ElementType.TRIANGLE)
    assert legacy.has_element_entity(2, 1, ElementType.QUADRANGLE)
    assert not legacy.has_element_entity(2, 1, ElementType.TETRAHEDRON)

    with pytest.raises(KeyError, match="ambiguous.*element_type"):
        legacy.get_element_entity(2, 1)

    triangle = legacy.get_element_entity(2, 1, ElementType.TRIANGLE)
    quadrangle = legacy.get_element_entity(2, 1, ElementType.QUADRANGLE)

    assert triangle.get_element_type() == ElementType.TRIANGLE
    assert triangle.get_number_of_elements() == 1
    assert triangle.get_element(1).get_connectivity() == [1, 2, 3]
    assert quadrangle.get_element_type() == ElementType.QUADRANGLE
    assert quadrangle.get_number_of_elements() == 1
    assert quadrangle.get_element(2).get_connectivity() == [1, 2, 4, 5]

    modern = gmshparser.read(path)

    assert modern.elements.tags == (1, 2)
    assert modern.element_types == frozenset(
        {ElementType.TRIANGLE, ElementType.QUADRANGLE}
    )
    assert modern.entity(2, 1).elements.tags == (1, 2)
    assert modern.entity(2, 1).element_types == modern.element_types

    arrays = gnp.to_numpy(modern)

    assert set(arrays.element_types) == {
        ElementType.TRIANGLE,
        ElementType.QUADRANGLE,
    }
    assert arrays.cells[ElementType.TRIANGLE].element_tags.tolist() == [1]
    assert arrays.cells[ElementType.TRIANGLE].connectivity.tolist() == [[0, 1, 2]]
    assert arrays.cells[ElementType.QUADRANGLE].element_tags.tolist() == [2]
    assert arrays.cells[ElementType.QUADRANGLE].connectivity.tolist() == [[0, 1, 3, 4]]
