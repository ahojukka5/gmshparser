from typing import TextIO

from .abstract_parser import AbstractParser
from .mesh import Mesh


class EntitiesParser(AbstractParser):
    """Parse MSH 4.x entity-to-physical-group assignments."""

    @staticmethod
    def get_section_name():
        return "$Entities"

    @staticmethod
    def parse(mesh: Mesh, io: TextIO) -> None:
        line = io.readline()
        if line.startswith("$Entities"):
            line = io.readline()

        counts = [int(value) for value in line.split()]
        if len(counts) != 4:
            raise ValueError("$Entities header must contain four entity counts")

        for dimension, count in enumerate(counts):
            physical_count_index = 4 if dimension == 0 else 7
            for _ in range(count):
                parts = io.readline().split()
                tag = int(parts[0])
                number_of_physical_tags = int(parts[physical_count_index])
                start = physical_count_index + 1
                stop = start + number_of_physical_tags
                mesh.set_entity_physical_tags(
                    dimension,
                    tag,
                    (int(value) for value in parts[start:stop]),
                )
