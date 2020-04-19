from gmshparser.mesh_format_parser import MeshFormatParser
from gmshparser.mesh import Mesh
import io


def test_mesh_format_parser():
    parser = MeshFormatParser()
    mesh = Mesh()
    data = io.StringIO("4.1 0 8")
    parser.parse(mesh, data)
    assert mesh.get_version() == 4.1
    assert mesh.get_ascii() is True
    assert mesh.get_precision() == 8
