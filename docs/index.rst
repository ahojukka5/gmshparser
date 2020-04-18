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

.. code-block:: python

   import gmshparser
   gmshparser.parse("testdata.msh")

Contributing to the project
---------------------------

Like in other open source projects, contributions are always welcome to this
too! If you have some great ideas how to make this package better, feature
requests etc., you can open an issue on gmshparser's `issue tracker`_ or
contact me (ahojukka5 at gmail.com) directly.

.. _issue tracker: https://github.com/ahojukka5/gmshparser/issues
.. _Gmsh: https://gmsh.info/
