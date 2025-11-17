from typing import TextIO
from .mesh import Mesh


class AbstractParser(object):
    """AbstractParser is a superclass of all other parsers.

    All other parsers must inheric ``AbstractParser`` and implement their own
    static methods ``parse`` and ``get_section_name``.

    The first argument of the ``parse`` is a mutable ``mesh`` object, which
    parser modifies in-place. The second argument is ``io``, where parser reads
    the text file line by line using `readline()`. Parser must stop reading the
    file to the section end mark, e.g. ``$EndNodes`` in the case of parser
    which is responsible to parse nodes, starting from a section start mark
    ``$Nodes``.

    Another must-to-implement static method is ``get_section_name()``, which
    must return the name of the line where this parser should activate. For
    example, if the section name is ``$Nodes``, then ``get_section_name()``
    must return string ``$Nodes``.
    """

    @staticmethod
    def get_section_name():
        raise NotImplementedError("Not implemented.")

    @staticmethod
    def parse(mesh: Mesh, io: TextIO) -> None:
        raise NotImplementedError("Not implemented.")
