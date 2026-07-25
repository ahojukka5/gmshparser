from __future__ import annotations

import pytest

from gmshparser.api import (
    ElementCollection,
    EntityCollection,
    NodeCollection,
    PhysicalGroup,
    PhysicalGroupCollection,
)


def _group(dimension: int, tag: int, name: str | None) -> PhysicalGroup:
    return PhysicalGroup(
        dimension=dimension,
        tag=tag,
        name=name,
        entities=EntityCollection(()),
        elements=ElementCollection(()),
        nodes=NodeCollection(()),
    )


def test_get_returns_group_for_key_and_unambiguous_name():
    boundary = _group(1, 10, "boundary")
    groups = PhysicalGroupCollection((boundary,))

    assert groups.get((1, 10)) is boundary
    assert groups.get("boundary") is boundary


def test_get_returns_default_only_when_key_is_absent():
    fallback = _group(0, 99, "fallback")
    groups = PhysicalGroupCollection((_group(1, 10, "boundary"),))

    assert groups.get((2, 20)) is None
    assert groups.get("missing") is None
    assert groups.get((2, 20), fallback) is fallback
    assert groups.get("missing", fallback) is fallback


def test_get_raises_for_ambiguous_name_even_when_default_is_given():
    fallback = _group(0, 99, "fallback")
    groups = PhysicalGroupCollection(
        (
            _group(1, 10, "wall"),
            _group(2, 20, "wall"),
        )
    )

    with pytest.raises(KeyError, match="ambiguous"):
        groups.get("wall")

    with pytest.raises(KeyError, match="ambiguous"):
        groups.get("wall", fallback)
