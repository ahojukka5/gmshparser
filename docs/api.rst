API Documentation
-----------------

.. py:currentmodule:: gmshparser

Externals
+++++++++

External classes and functions are the public API of the package.

The main command used to parse mesh is `gmshparser.parse`.

.. autofunction:: gmshparser.parse

Package contains data structures to describe nodes, node entities,
elements and element entities.

.. autoclass:: gmshparser.node.Node
   :members:

.. autoclass:: gmshparser.node_entity.NodeEntity
   :members:

.. autoclass:: gmshparser.element.Element
   :members:

.. autoclass:: gmshparser.element_entity.ElementEntity
   :members:

The main class is `Mesh`, which collects everything together.

.. autoclass:: gmshparser.mesh.Mesh
   :members:

Internals
+++++++++

Internal classes and functions are the private API of the package. They can
change without any warning.

Functions
*********

.. autofunction:: gmshparser.helpers.parse_ints

.. autofunction:: gmshparser.helpers.parse_floats

.. autofunction:: parse_io

Classes
*******

Parsers must be inherited from `AbstractParser` and they must implement
function `parse`, which is responsible of parsing a section.

.. autoclass:: gmshparser.abstract_parser.AbstractParser
   :members:

.. autoclass:: gmshparser.mesh_format_parser.MeshFormatParser
   :members:

.. autoclass:: gmshparser.nodes_parser.NodesParser
   :members:

.. autoclass:: gmshparser.elements_parser.ElementsParser
   :members:
