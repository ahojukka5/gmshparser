from io import StringIO

import pytest

import gmshparser

MESH = """$MeshFormat
4.1 0 8
$EndMeshFormat
$PhysicalNames
1
0 7 "Probe"
$EndPhysicalNames
$Entities
2 0 0 0
1 0 0 0 1 7
2 1 0 0 1 8
$EndEntities
"""


def _read_direct(source: str):
    return gmshparser.read(StringIO(source), name="declared-entities.msh")


def _read_through_legacy(source: str):
    legacy = gmshparser.Mesh()
    legacy.set_name("declared-entities.msh")
    gmshparser.MainParser().parse(legacy, StringIO(source))
    return gmshparser.ModernMesh.from_legacy(legacy)


@pytest.mark.parametrize("loader", [_read_direct, _read_through_legacy])
def test_declared_entities_survive_without_mesh_blocks(loader):
    mesh = loader(MESH)

    probe_entity = mesh.entities[(0, 1)]
    anonymous_entity = mesh.entities[(0, 2)]

    assert len(mesh.entities) == 2
    assert probe_entity.physical_tags == (7,)
    assert probe_entity.bounding_box == (0.0, 0.0, 0.0, 0.0, 0.0, 0.0)
    assert probe_entity.boundary_tags == ()
    assert anonymous_entity.physical_tags == (8,)
    assert anonymous_entity.bounding_box == (1.0, 0.0, 0.0, 1.0, 0.0, 0.0)
    assert anonymous_entity.boundary_tags == ()
    assert len(probe_entity.nodes) == 0
    assert len(probe_entity.elements) == 0

    probe = mesh.physical_groups["Probe"]
    anonymous = mesh.physical_groups[(0, 8)]

    assert probe.entities[(0, 1)] is probe_entity
    assert anonymous.name is None
    assert anonymous.entities[(0, 2)] is anonymous_entity
    assert len(probe.nodes) == 0
    assert len(probe.elements) == 0


VOLUME = """$MeshFormat
4.1 0 8
$EndMeshFormat
$Entities
0 0 0 1
1 0 0 0 1 2 3 1 5 6 1 -2 3 -4 5 -6
$EndEntities
"""


@pytest.mark.parametrize("loader", [_read_direct, _read_through_legacy])
def test_volume_entity_keeps_box_and_boundary_tags(loader):
    volume = loader(VOLUME).entities[(3, 1)]

    assert volume.bounding_box == (0.0, 0.0, 0.0, 1.0, 2.0, 3.0)
    assert volume.boundary_tags == (1, -2, 3, -4, 5, -6)
    assert volume.physical_tags == (5,)
