from gmshparser.cli import main
from io import StringIO
import os

__content__ = """
$MeshFormat
4.1 0 8
$EndMeshFormat
$Nodes
1 6 1 6
2 1 0 6
1
2
3
4
5
6
0. 0. 0.
1. 0. 0.
1. 1. 0.
0. 1. 0.
2. 0. 0.
2. 1. 0.
$EndNodes
$Elements
1 2 1 2
2 1 3 2
1 1 2 3 4
2 2 5 6 3
$EndElements
$NodeData
1
"A scalar view"
1
0.0
3
0
1
6
1 0.0
2 0.1
3 0.2
4 0.0
5 0.2
6 0.4
$EndNodeData
"""


def test_main(tmpdir):
    fh = tmpdir.join("mesh1.msh")
    fh.write(__content__.strip())
    filename = os.path.join(fh.dirname, fh.basename)
    # We just check that there comes some print from functions to stdout

    output = StringIO()
    main([filename, "info"], output)
    assert len(output.getvalue()) == 288

    output = StringIO()
    main([filename, "nodes"], output)
    assert len(output.getvalue()) == 176

    output = StringIO()
    main([filename, "elements"], output)
    assert len(output.getvalue()) == 26
