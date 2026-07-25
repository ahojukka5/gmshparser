from pathlib import Path
from typing import assert_type

import gmshparser
from gmshparser.api import (
    Element,
    ElementCollection,
    Entity,
    EntityCollection,
    Mesh,
    Node,
    NodeCollection,
    PeriodicLink,
    PeriodicLinkCollection,
    PhysicalGroup,
    PhysicalGroupCollection,
)


def verify_public_api(path: Path) -> None:
    modern = gmshparser.read(path)
    assert_type(modern, Mesh)
    assert_type(modern.nodes, NodeCollection)
    assert_type(modern.elements, ElementCollection)
    assert_type(modern.entities, EntityCollection)
    assert_type(modern.physical_groups, PhysicalGroupCollection)
    assert_type(modern.periodic_links, PeriodicLinkCollection)

    assert_type(modern.nodes[1], Node)
    assert_type(modern.nodes.get(1), Node | None)
    assert_type(modern.nodes.by_entity(2, 7), NodeCollection)
    assert_type(modern.elements[1], Element)
    assert_type(
        modern.elements.by_type(gmshparser.ElementType.TRIANGLE),
        ElementCollection,
    )
    assert_type(modern.entity(2, 7), Entity)
    assert_type(modern.entities.by_dimension(2), EntityCollection)
    assert_type(modern.physical_group("Walls"), PhysicalGroup)
    assert_type(modern.physical_groups.by_dimension(2), PhysicalGroupCollection)
    assert_type(modern.periodic_link(2, 7), PeriodicLink)
    assert_type(modern.periodic_links.by_dimension(2), PeriodicLinkCollection)
    assert_type(modern.surfaces, EntityCollection)
    assert_type(modern.dimension, int | None)
    assert_type(
        modern.bounds,
        tuple[tuple[float, float, float], tuple[float, float, float]] | None,
    )

    compatibility = gmshparser.parse(str(path))
    assert_type(compatibility, gmshparser.Mesh)
