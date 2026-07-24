from typing import TextIO

from .abstract_parser import AbstractParser
from .errors import InvalidSectionError
from .mesh import Mesh
from .parsing import expect_end_marker, read_required_line


class EntitiesParser(AbstractParser):
    """Parse MSH 4.x entity-to-physical-group assignments."""

    @staticmethod
    def get_section_name():
        return "$Entities"

    @staticmethod
    def parse(mesh: Mesh, io: TextIO) -> None:
        line = read_required_line(io, "$Entities header")
        if line.startswith("$Entities"):
            line = read_required_line(io, "$Entities header")

        try:
            counts = [int(value) for value in line.split()]
        except ValueError as error:
            raise InvalidSectionError(
                "$Entities header must contain integers"
            ) from error
        if len(counts) != 4:
            raise InvalidSectionError(
                "$Entities header must contain four entity counts"
            )
        if any(count < 0 for count in counts):
            raise InvalidSectionError("$Entities counts cannot be negative")

        for dimension, count in enumerate(counts):
            physical_count_index = 4 if dimension == 0 else 7
            for _ in range(count):
                record = read_required_line(io, "an entity record")
                parts = record.split()
                minimum_fields = physical_count_index + 1
                if len(parts) < minimum_fields:
                    raise InvalidSectionError(
                        f"A dimension-{dimension} entity record requires at least "
                        f"{minimum_fields} fields"
                    )

                try:
                    tag = int(parts[0])
                    number_of_physical_tags = int(parts[physical_count_index])
                except ValueError as error:
                    raise InvalidSectionError(
                        "Entity tags and physical-group counts must be integers"
                    ) from error
                if number_of_physical_tags < 0:
                    raise InvalidSectionError(
                        "Entity physical-group counts cannot be negative"
                    )

                start = physical_count_index + 1
                stop = start + number_of_physical_tags
                if len(parts) < stop:
                    raise InvalidSectionError(
                        f"Entity {tag} declares {number_of_physical_tags} physical "
                        f"tags, but the record contains {max(0, len(parts) - start)}"
                    )

                try:
                    physical_tags = tuple(int(value) for value in parts[start:stop])
                except ValueError as error:
                    raise InvalidSectionError(
                        "Entity physical-group tags must be integers"
                    ) from error
                mesh.set_entity_physical_tags(dimension, tag, physical_tags)

        expect_end_marker(io, "$EndEntities")
