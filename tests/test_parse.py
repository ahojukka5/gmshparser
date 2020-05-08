from gmshparser import parse
import os

__content__ = """
$MeshFormat
4.1 0 8
$EndMeshFormat
"""


def test_parse(tmpdir):
    fh = tmpdir.join("mesh1.msh")
    fh.write(__content__.strip())
    filename = os.path.join(fh.dirname, fh.basename)
    mesh = parse(filename)
    assert mesh.get_name().endswith("mesh1.msh")
    assert mesh.get_version() == 4.1
