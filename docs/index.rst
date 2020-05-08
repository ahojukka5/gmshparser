Welcome to gmshparser's documentation!
======================================

Package author: Jukka Aho (`@ahojukka5 <https://github.com/ahojukka5>`_)

Gmshparser is a small Python package which aims to do only one thing: parse `Gmsh`_
mesh file format. Package does not have any external dependencies to other
packages and it aims to be a simple stand-alone solution for a common problem:
how to import mesh to your favourite research FEM code?

Project is hosted on GitHub: https://github.com/ahojukka5/gmshparser. Project is
licensed under MIT license. Please see the :doc:`project license <license>` for
further details.

.. toctree::
   :hidden:
   :maxdepth: 2

   Home <self>
   Mesh formats <mesh_formats>
   API <api>
   License <license>

Installing package
------------------

Package can be installed using a standard package installing tool pip:

.. code-block:: bash

   pip install gmshparser

Development version can be installed from GitHub repository, again, using pip:

.. code-block:: bash

   pip install git+git://github.com/ahojukka5/gmshparser.git

Usage
-----

The usage of the package is quite straightforward. Import libary and read mesh
using ``gmshparser.parse``, given the filename of the mesh:

.. code-block:: python

   import gmshparser
   mesh = gmshparser.parse("data/testmesh.msh")
   print(mesh)

Output:

.. code-block:: none

   Mesh name: data/testmesh.msh
   Mesh version: 4.1
   Number of nodes: 6
   Minimum node tag: 1
   Maximum node tag: 6
   Number of node entities: 1
   Number of elements: 2
   Minimum element tag: 1
   Maximum element tag: 2
   Number of element entities: 1

All nodes are stored in node entities and all elements are stored in element
entities. To access nodes, one must first loop all node entities and after
that all nodes in node entity::

   for entity in mesh.get_node_entities():
       for node in entity.get_nodes():
           nid = node.get_tag()
           ncoords = node.get_coordinates()
           print("Node id = %s, node coordinates = %s" % (nid, ncoords))

Output:

.. code-block:: none

   Node id = 1, node coordinates = (0.0, 0.0, 0.0)
   Node id = 2, node coordinates = (1.0, 0.0, 0.0)
   Node id = 3, node coordinates = (1.0, 1.0, 0.0)
   Node id = 4, node coordinates = (0.0, 1.0, 0.0)
   Node id = 5, node coordinates = (2.0, 0.0, 0.0)
   Node id = 6, node coordinates = (2.0, 1.0, 0.0)

Accessing elements is done in a similar way, first entities and then elements.
Element type is given in each entity. For example, here code 3 means linear
quadrangle::

   for entity in mesh.get_element_entities():
       eltype = entity.get_element_type()
       print("Element type: %s" % eltype)
       for element in entity.get_elements():
           elid = element.get_tag()
           elcon = element.get_connectivity()
           print("Element id = %s, connectivity = %s" % (elid, elcon))

Output:

.. code-block:: none

   Element type: 3
   Element id = 1, connectivity = [1, 2, 3, 4]
   Element id = 2, connectivity = [2, 5, 6, 3]

Contributing to the project
---------------------------

Like in other open source projects, contributions are always welcome to this
too! If you have some great ideas how to make this package better, feature
requests etc., you can open an issue on gmshparser's `issue tracker`_ or
contact me (ahojukka5 at gmail.com) directly.

.. _issue tracker: https://github.com/ahojukka5/gmshparser/issues
.. _Gmsh: https://gmsh.info/
