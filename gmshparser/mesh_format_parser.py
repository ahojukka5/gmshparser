from typing import TextIO
from .abstract_parser import AbstractParser
from .mesh import Mesh


class MeshFormatParser(AbstractParser):

    @staticmethod
    def get_section_name():
        return "$MeshFormat"

    @staticmethod
    def parse(mesh: Mesh, io: TextIO) -> None:
        s = io.readline().strip().split(" ")
        mesh.set_version(float(s[0]))
        mesh.set_ascii(int(s[1]) == 0)
        mesh.set_precision(int(s[2]))
