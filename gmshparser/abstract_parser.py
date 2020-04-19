from typing import TextIO
from .mesh import Mesh


class AbstractParser(object):
    def parse(self, mesh: Mesh, io: TextIO) -> None:
        raise NotImplementedError(
            "You have to implement parser(self, mesh, io) to your parser")
