import shlex
from typing import TextIO

from .abstract_parser import AbstractParser
from .mesh import Mesh


class PhysicalNamesParser(AbstractParser):
    """Parse optional ``$PhysicalNames`` declarations."""

    @staticmethod
    def get_section_name():
        return "$PhysicalNames"

    @staticmethod
    def parse(mesh: Mesh, io: TextIO) -> None:
        line = io.readline()
        if line.startswith("$PhysicalNames"):
            line = io.readline()

        count = int(line.strip())
        for _ in range(count):
            dimension, tag, name = shlex.split(io.readline().strip(), posix=True)
            mesh.set_physical_name(int(dimension), int(tag), name)
