from __future__ import annotations

from io import StringIO

import pytest

import gmshparser


def _msh41(entities: str) -> str:
    return f"""$MeshFormat
4.1 0 8
$EndMeshFormat
$Entities
{entities}
$EndEntities
"""


def test_entities_accept_signed_references_to_declared_boundaries():
    source = _msh41(
        """2 1 0 0
1 0 0 0 0
2 1 0 0 0
7 0 0 0 1 0 0 0 2 1 -2"""
    )

    mesh = gmshparser.read(StringIO(source), name="oriented-boundary.msh")

    assert len(mesh.nodes) == 0
    assert len(mesh.elements) == 0


def test_entities_accept_boundaries_declared_in_a_repeated_section():
    source = _msh41("1 0 0 0\n1 0 0 0 0") + """$Entities
0 1 0 0
7 0 0 0 1 0 0 0 1 1
$EndEntities
"""

    mesh = gmshparser.read(StringIO(source), name="repeated-entities.msh")

    assert len(mesh.nodes) == 0
    assert len(mesh.elements) == 0


def test_entities_reject_duplicate_tags_within_a_dimension():
    source = _msh41(
        """2 0 0 0
1 0 0 0 0
1 1 0 0 0"""
    )

    with pytest.raises(
        gmshparser.InvalidSectionError,
        match="Duplicate dimension-0 entity tag 1",
    ):
        gmshparser.read(StringIO(source), name="duplicate-entity.msh")


def test_entities_reject_non_finite_geometry_values():
    source = _msh41(
        """1 0 0 0
1 nan 0 0 0"""
    )

    with pytest.raises(
        gmshparser.InvalidSectionError,
        match="Entity 1 contains non-finite geometry values",
    ):
        gmshparser.read(StringIO(source), name="non-finite-entity.msh")


def test_entities_reject_inverted_bounding_boxes():
    source = _msh41(
        """2 1 0 0
1 0 0 0 0
2 1 0 0 0
7 1 0 0 0 0 0 0 2 1 2"""
    )

    with pytest.raises(
        gmshparser.InvalidSectionError,
        match="Entity 7 has an inverted bounding box",
    ):
        gmshparser.read(StringIO(source), name="inverted-bounds.msh")


def test_entities_reject_non_positive_physical_tags():
    source = _msh41(
        """1 0 0 0
1 0 0 0 1 0"""
    )

    with pytest.raises(
        gmshparser.InvalidSectionError,
        match="Entity physical-group tags must be positive integers",
    ):
        gmshparser.read(StringIO(source), name="invalid-physical-tag.msh")
