from io import StringIO

import pytest

import gmshparser
from gmshparser.api import Mesh as ModernMesh
from gmshparser.main_parser import MainParser
from gmshparser.mesh import Mesh as LegacyMesh

MSH_1 = """$NOD
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

MSH_2 = """$MeshFormat
2.2 0 8
$EndMeshFormat
$PhysicalNames
1
2 99 "Surface"
$EndPhysicalNames
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

MSH_4 = """$MeshFormat
4.1 0 8
$EndMeshFormat
$PhysicalNames
1
2 99 "Surface"
$EndPhysicalNames
$Entities
0 0 1 0
1 0 0 0 2 1 0 1 99
$EndEntities
$Nodes
1 5 1 5
2 1 0 5
1
2
3
4
5
0.0 0.0 0.0
1.0 0.0 0.0
0.0 1.0 0.0
1.0 1.0 0.0
2.0 1.0 0.0
$EndNodes
$Elements
2 2 1 2
2 1 2 1
1 1 2 3
2 1 3 1
2 1 2 4 5
$EndElements
"""


def _legacy_modern(content: str, name: str) -> ModernMesh:
    legacy = LegacyMesh()
    legacy.set_name(name)
    MainParser().parse(legacy, StringIO(content))
    return ModernMesh.from_legacy(legacy)


def _snapshot(mesh: ModernMesh):
    return {
        "name": mesh.name,
        "version": mesh.version,
        "is_ascii": mesh.is_ascii,
        "data_size": mesh.data_size,
        "nodes": [
            (
                node.tag,
                node.coordinates,
                node.dimension,
                node.entity_tag,
                node.parametric_coordinates,
                node.physical_tags,
            )
            for node in mesh.nodes
        ],
        "elements": [
            (
                element.tag,
                int(element.element_type),
                element.node_tags,
                element.dimension,
                element.entity_tag,
                element.physical_tags,
            )
            for element in mesh.elements
        ],
        "entities": [
            (
                entity.dimension,
                entity.tag,
                entity.nodes.tags,
                entity.elements.tags,
                entity.physical_tags,
            )
            for entity in mesh.entities
        ],
        "physical_groups": [
            (
                group.dimension,
                group.tag,
                group.name,
                group.entities.keys,
                group.elements.tags,
                group.nodes.tags,
            )
            for group in mesh.physical_groups
        ],
    }


@pytest.mark.parametrize(
    ("name", "content"),
    [
        ("legacy.msh", MSH_1),
        ("flat.msh", MSH_2),
        ("blocks.msh", MSH_4),
    ],
)
def test_direct_builder_matches_legacy_conversion(name, content):
    expected = _legacy_modern(content, name)
    actual = gmshparser.read(StringIO(content), name=name)

    assert _snapshot(actual) == _snapshot(expected)


def test_read_does_not_call_mesh_from_legacy(monkeypatch):
    def fail_from_legacy(cls, legacy):
        raise AssertionError("read() must not build through the compatibility mesh")

    monkeypatch.setattr(ModernMesh, "from_legacy", classmethod(fail_from_legacy))

    mesh = gmshparser.read(StringIO(MSH_2), name="direct.msh")

    assert mesh.name == "direct.msh"
    assert mesh.elements.tags == (1, 2)
