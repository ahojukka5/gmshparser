from pathlib import Path
from typing import assert_type

import gmshparser
from gmshparser.api import (
    ElementCollection,
    EntityCollection,
    Mesh,
    NodeCollection,
    PeriodicLinkCollection,
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

    compatibility = gmshparser.parse(str(path))
    assert_type(compatibility, gmshparser.Mesh)
