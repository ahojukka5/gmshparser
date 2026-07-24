from io import StringIO

import gmshparser
from gmshparser.api import ElementType, Mesh as ModernMesh, parse as parse_modern

MSH2 = """$MeshFormat
2.1 0 8
$EndMeshFormat
$PhysicalNames
2
1 10 "Left Edge"
2 20 "Surface"
$EndPhysicalNames
$Nodes
4
1 0 0 0
2 1 0 0
3 1 1 0
4 0 1 0
$EndNodes
$Elements
2
1 1 2 10 2 1 2
2 2 2 20 3 1 2 3
$EndElements
"""

MSH4 = """$MeshFormat
4.1 0 8
$EndMeshFormat
$PhysicalNames
2
2 11 "Wall"
3 22 "Domain"
$EndPhysicalNames
$Entities
0 0 1 1
1 0 0 0 1 1 0 1 11 0
1 0 0 0 1 1 1 1 22 0
$EndEntities
$Nodes
2 4 1 4
2 1 0 3
1
2
3
0 0 0
1 0 0
0 1 0
3 1 0 1
4
0 0 1
$EndNodes
$Elements
2 2 1 2
2 1 2 1
1 1 2 3
3 1 4 1
2 1 2 3 4
$EndElements
"""


def test_msh2_physical_names_and_element_tags_are_preserved():
    mesh = gmshparser.read(StringIO(MSH2))

    left = mesh.physical_groups["Left Edge"]
    surface = mesh.physical_group("Surface")

    assert left.key == (1, 10)
    assert left.elements.tags == (1,)
    assert left.nodes.tags == (1, 2)
    assert surface.key == (2, 20)
    assert surface.elements.tags == (2,)
    assert surface.elements[2].physical_tags == (20,)


def test_msh4_entities_resolve_to_named_physical_groups():
    mesh = gmshparser.read(StringIO(MSH4))

    wall = mesh.physical_groups[(2, 11)]
    domain = mesh.physical_groups["Domain"]

    assert wall.name == "Wall"
    assert wall.entities.keys == ((2, 1),)
    assert wall.elements.tags == (1,)
    assert wall.nodes.tags == (1, 2, 3)
    assert domain.entities.keys == ((3, 1),)
    assert domain.elements.tags == (2,)
    assert domain.nodes.tags == (4, 1, 2, 3)


def test_entity_helpers_and_element_type_naming_are_pythonic():
    mesh = gmshparser.read(StringIO(MSH4))

    assert mesh.entity(2, 1) is mesh.entities[(2, 1)]
    assert mesh.surfaces.keys == ((2, 1),)
    assert mesh.volumes.keys == ((3, 1),)
    assert mesh.elements.by_entity(2, 1).tags == (1,)
    assert mesh.nodes.by_entity(2, 1).tags == (1, 2, 3)

    element = mesh.elements[1]
    assert element.element_type is ElementType.TRIANGLE
    assert element.type is ElementType.TRIANGLE


def test_explicit_api_parse_returns_modern_mesh_without_changing_top_level_parse(
    tmp_path,
):
    modern = parse_modern(StringIO(MSH4))
    assert isinstance(modern, ModernMesh)

    path = tmp_path / "mesh.msh"
    path.write_text(MSH4)
    legacy = gmshparser.parse(str(path))

    assert isinstance(legacy, gmshparser.Mesh)
    assert not isinstance(legacy, ModernMesh)
