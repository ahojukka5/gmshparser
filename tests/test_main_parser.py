from gmshparser import MainParser
from gmshparser.mesh import Mesh
from io import StringIO
from pytest import raises


__content__ = """
$MeshFormat
4.1 0 8
$EndMeshFormat
$Unknown
my custom data
$EndUnknown
"""


__bad_content__ = """
$MeshFormat
4.1 0 8          MSH4.1, ASCII
$EndMeshFormat
$Nodes
1 6 1 6          1 entity bloc, 6 nodes total, min/max node tags: 1 and 6
2 1 0 6          2D entity (surface) 1, no parametric coordinates, 6 nodes
$EndNodes
""".strip()


def test_mainparser():
    parser = MainParser()
    mesh = Mesh()
    parser.parse(mesh, StringIO(__content__))
    assert mesh.get_version() == 4.1


def test_parse_io_bad_content():
    parser = MainParser()
    mesh = Mesh()
    with raises(Exception):
        parser.parse(mesh, StringIO(__bad_content__))
