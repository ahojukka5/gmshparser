Mesh formats
------------

Mesh formats can be found from: https://gmsh.info/doc/texinfo/gmsh.html#MSH-file-format

Format 4.1
++++++++++

.. code-block::

    $MeshFormat
    4.1 0 8          MSH4.1, ASCII
    $EndMeshFormat
    $Nodes
    1 6 1 6          1 entity bloc, 6 nodes total, min/max node tags: 1 and 6
    2 1 0 6          2D entity (surface) 1, no parametric coordinates, 6 nodes
    1                  node tag #1
    2                  node tag #2
    3                  etc.
    4
    5
    6
    0. 0. 0.           node #1 coordinates (0., 0., 0.)
    1. 0. 0.           node #2 coordinates (1., 0., 0.)
    1. 1. 0.           etc.
    0. 1. 0.
    2. 0. 0.
    2. 1. 0.
    $EndNodes
    $Elements
    1 2 1 2          1 entity bloc, 2 elements total, min/max element tags: 1 and 2
    2 1 3 2          2D entity (surface) 1, element type 3 (4-node quad), 2 elements
    1 1 2 3 4          quad tag #1, nodes 1 2 3 4
    2 2 5 6 3          quad tag #2, nodes 2 5 6 3
    $EndElements
    $NodeData
    1                1 string tag:
    "A scalar view"    the name of the view ("A scalar view")
    1                1 real tag:
    0.0                the time value (0.0)
    3                3 integer tags:
    0                  the time step (0; time steps always start at 0)
    1                  1-component (scalar) field
    6                  6 associated nodal values
    1 0.0            value associated with node #1 (0.0)
    2 0.1            value associated with node #2 (0.1)
    3 0.2            etc.
    4 0.0
    5 0.2
    6 0.4
    $EndNodeData
