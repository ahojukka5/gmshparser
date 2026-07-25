from __future__ import annotations

from io import StringIO

import pytest

import gmshparser
from gmshparser.api import Mesh as ModernMesh

AFFINE = "1 0 0 1 0 1 0 0 0 0 1 0 0 0 0 1"

MSH4 = f"""$MeshFormat
4.1 0 8
$EndMeshFormat
$Nodes
2 4 1 4
1 1 0 2
1
2
0 0 0
0 1 0
1 2 0 2
3
4
1 0 0
1 1 0
$EndNodes
$Elements
0 0 0 0
$EndElements
$Periodic
2
1 2 1
0
2
3 1
4 2
1 4 3
16 {AFFINE}
1
4 2
$EndPeriodic
"""

MSH2 = f"""$MeshFormat
2.2 0 8
$EndMeshFormat
$Nodes
4
1 0 0 0
2 0 1 0
3 1 0 0
4 1 1 0
$EndNodes
$Elements
0
$EndElements
$Periodic
2
1 2 1
2
3 1
4 2
1 4 3
Affine {AFFINE}
1
4 2
$EndPeriodic
"""


@pytest.mark.parametrize("content", [MSH2, MSH4])
def test_periodic_links_are_available_in_modern_and_legacy_models(tmp_path, content):
    path = tmp_path / "periodic.msh"
    path.write_text(content)

    modern = gmshparser.read(path)
    legacy = gmshparser.parse(str(path))
    converted = ModernMesh.from_legacy(legacy)

    first = modern.periodic_links[(1, 2)]
    assert first.key == (1, 2)
    assert first.master_entity_tag == 1
    assert first.affine_transform == ()
    assert first.node_pairs == ((3, 1), (4, 2))
    assert first.slave_node_tags == (3, 4)
    assert first.master_node_tags == (1, 2)
    assert modern.periodic_link(1, 2) is first

    second = modern.periodic_links[(1, 4)]
    assert second.master_entity_tag == 3
    assert second.affine_transform == tuple(float(value) for value in AFFINE.split())
    assert second.node_pairs == ((4, 2),)

    assert modern.periodic_links.keys == ((1, 2), (1, 4))
    assert modern.periodic_links.by_dimension(1) == modern.periodic_links
    assert modern.periodic_links.where(dimension=2).keys == ()

    assert legacy.get_periodic_link(1, 2) == (1, (), ((3, 1), (4, 2)))
    assert legacy.get_periodic_links()[1][2:] == (
        3,
        tuple(float(value) for value in AFFINE.split()),
        ((4, 2),),
    )
    assert converted.periodic_links == modern.periodic_links


def test_v4_affine_values_can_continue_on_following_lines():
    content = MSH4.replace(
        f"16 {AFFINE}",
        "16 1 0 0 1 0 1 0 0\n0 0 1 0 0 0 0 1",
    )

    link = gmshparser.read(StringIO(content)).periodic_links[(1, 4)]

    assert link.affine_transform == tuple(float(value) for value in AFFINE.split())


def test_duplicate_periodic_slave_entity_is_rejected():
    duplicate = MSH4.replace("1 4 3", "1 2 3")

    with pytest.raises(gmshparser.InvalidSectionError, match="Duplicate periodic link"):
        gmshparser.read(StringIO(duplicate), name="duplicate.msh")


def test_truncated_periodic_node_pairs_report_source_context():
    truncated = MSH4.replace("4 2\n$EndPeriodic\n", "")

    with pytest.raises(gmshparser.UnexpectedEndOfFileError) as caught:
        gmshparser.read(StringIO(truncated), name="truncated.msh")

    assert caught.value.filename == "truncated.msh"
    assert caught.value.section == "$Periodic"


def test_unknown_periodic_master_node_is_rejected_by_modern_builder():
    invalid = MSH4.replace("4 2\n$EndPeriodic", "4 999\n$EndPeriodic")

    with pytest.raises(gmshparser.InvalidMeshError, match="unknown master node 999"):
        gmshparser.read(StringIO(invalid), name="unknown-node.msh")


def test_negative_corresponding_node_count_is_rejected():
    invalid = MSH4.replace(f"16 {AFFINE}\n1\n4 2", f"16 {AFFINE}\n-1")

    with pytest.raises(
        gmshparser.InvalidSectionError,
        match="corresponding-node count cannot be negative",
    ):
        gmshparser.read(StringIO(invalid), name="negative-count.msh")
