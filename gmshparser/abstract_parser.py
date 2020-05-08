from typing import TextIO
from .mesh import Mesh


class AbstractParser(object):

    """ AbstractParser is a superclass of all other parsers.

    All other parsers must inheric ``AbstractParser`` and implement their own
    ``parse`` method.

    The first argument of the parse is a mutable ``mesh`` object, which parser
    modifies in-place. The second argument is ``io``, where parser reads the
    text file line by line using `readline()`. Parser must stop reading the
    file to the section end mark, e.g. ``$EndNodes`` in the case of parser
    which is responsible to parse nodes, starting from a section start mark
    ``$Nodes$``.
    """

    def parse(self, mesh: Mesh, io: TextIO) -> None:
        raise NotImplementedError("Not implemented.")
