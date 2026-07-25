from __future__ import annotations

from io import StringIO

import pytest

import gmshparser
from gmshparser.api import Mesh as ModernMesh


MSH40 = """$MeshFormat
4.0 0 8
$EndMeshFormat
$PhysicalNames
2
0 7 "Origin"
2 11 "Surface"
$EndPhysicalNames
$Entities
1 0 1 0
1 0 0 0 0 0 0 1 7
1 0 0 0 1 1 0 1 11 0
$EndEntities
$Nodes
2 4
1 0 0 1
1 0 0 0
1 2 0 3
2 1 0 0
3 1 1 0
4 0 1 0
$EndNodes
$Elements
2 2
1 0 15 1
1 1
1 2 2 1
2 2 3 4
$EndElements
"""

AFFINE = "1 0 0 1 0 1 0 0 0 0 1 0 0 0 0 1"

MSH40_PERIODIC = f"""$MeshFormat
4.0 0 8
$EndMeshFormat
$Entities
0 2 0 0
1 0 0 0 0 1 0 0 0
2 1 0 0 1 1 0 0 0
$EndEntities
$Nodes
2 4
1 1 0 2
1 0 0 0
2 0 1 0
2 1 0 2
3 1 0 0
4 1 1 0
$EndNodes
$Elements
0 0
$EndElements
$Periodic
1
1 2 1
Affine {AFFINE}
2
3 1
4 2
$EndPeriodic
"""


def test_msh40_layout_is_preserved_in_modern_and_legacy_models(tmp_path):
    path = tmp_path / "mesh40.msh"
    path.write_text(MSH40)

    modern = gmshparser.read(path)
    legacy = gmshparser.parse(str(path))
    converted = ModernMesh.from_legacy(legacy)

    assert str(modern.version) == "4.0"
    assert modern.nodes.tags == (1, 2, 3, 4)
    assert modern.elements.tags == (1, 2)
    assert modern.entities.keys == ((0, 1), (2, 1))

    origin = modern.physical_groups["Origin"]
    assert origin.key == (0, 7)
    assert origin.entities.keys == ((0, 1),)
    assert origin.elements.tags == (1,)
    assert origin.nodes.tags == (1,)

    surface = modern.physical_groups["Surface"]
    assert surface.key == (2, 11)
    assert surface.entities.keys == ((2, 1),)
    assert surface.elements.tags == (2,)
    assert surface.nodes.tags == (2, 3, 4)

    assert legacy.get_min_node_tag() == 1
    assert legacy.get_max_node_tag() == 4
    assert legacy.get_min_element_tag() == 1
    assert legacy.get_max_element_tag() == 2
    assert converted == modern


def test_msh40_periodic_uses_optional_affine_record():
    modern = gmshparser.read(StringIO(MSH40_PERIODIC), name="periodic40.msh")

    link = modern.periodic_link(1, 2)
    assert link.master_entity_tag == 1
    assert link.affine_transform == tuple(float(value) for value in AFFINE.split())
    assert link.node_pairs == ((3, 1), (4, 2))


def test_msh40_entity_boundary_count_is_validated():
    malformed = MSH40.replace(
        "1 0 0 0 1 1 0 1 11 0",
        "1 0 0 0 1 1 0 1 11 2 1",
    )

    with pytest.raises(
        gmshparser.InvalidSectionError,
        match="declares 2 boundary tags, but the record contains 1",
    ):
        gmshparser.read(StringIO(malformed), name="bad-entities.msh")


def test_msh40_node_header_rejects_msh41_tag_range_fields():
    malformed = MSH40.replace("$Nodes\n2 4", "$Nodes\n2 4 1 4")

    with pytest.raises(
        gmshparser.InvalidNodeError,
        match="MSH 4.0 must contain 2 integers",
    ):
        gmshparser.read(StringIO(malformed), name="bad-nodes.msh")
