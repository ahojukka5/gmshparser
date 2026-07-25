from typing import TextIO

from .mesh import Mesh


class AbstractParser:
    """AbstractParser is a superclass of section parsers.

    Section parsers inherit ``AbstractParser`` and implement the static methods
    ``parse`` and ``get_section_name``.

    The first argument of ``parse`` is a mutable mesh object that the parser
    modifies in place. The second argument is the text stream. A section parser
    consumes input through its matching end marker, such as ``$EndNodes``.
    """

    @staticmethod
    def get_section_name() -> str:
        """Return the MSH section header handled by this parser."""
        raise NotImplementedError("Not implemented.")

    @staticmethod
    def parse(mesh: Mesh, io: TextIO) -> None:
        """Parse one section into the mutable target mesh."""
        raise NotImplementedError("Not implemented.")
