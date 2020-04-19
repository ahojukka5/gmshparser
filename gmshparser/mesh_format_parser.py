from typing import TextIO
from .abstract_parser import AbstractParser
from .mesh import Mesh


class MeshFormatParser(AbstractParser):
    def parse(self, mesh: Mesh, io: TextIO) -> None:
        s = io.readline().strip().split(" ")
        mesh.set_version(float(s[0]))
        mesh.set_ascii(int(s[1]) == 0)
        mesh.set_precision(int(s[2]))
