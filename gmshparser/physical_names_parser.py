import shlex
from typing import TextIO

from .abstract_parser import AbstractParser
from .errors import InvalidSectionError
from .mesh import Mesh
from .parsing import expect_end_marker, read_required_line


class PhysicalNamesParser(AbstractParser):
    """Parse optional ``$PhysicalNames`` declarations."""

    @staticmethod
    def get_section_name() -> str:
        return "$PhysicalNames"

    @staticmethod
    def parse(mesh: Mesh, io: TextIO) -> None:
        line = read_required_line(io, "$PhysicalNames count")
        if line.startswith("$PhysicalNames"):
            line = read_required_line(io, "$PhysicalNames count")

        try:
            count = int(line.strip())
        except ValueError as error:
            raise InvalidSectionError(
                "$PhysicalNames count must be an integer"
            ) from error
        if count < 0:
            raise InvalidSectionError("$PhysicalNames count cannot be negative")

        for _ in range(count):
            record = read_required_line(io, "a physical-name record")
            try:
                fields = shlex.split(record.strip(), posix=True)
            except ValueError as error:
                raise InvalidSectionError(
                    "A physical-name record contains invalid quoting"
                ) from error
            if len(fields) != 3:
                raise InvalidSectionError(
                    "A physical-name record must contain dimension, tag, and name"
                )

            dimension, tag, name = fields
            try:
                dimension_value = int(dimension)
                tag_value = int(tag)
            except ValueError as error:
                raise InvalidSectionError(
                    "Physical-name dimensions and tags must be integers"
                ) from error
            if dimension_value not in {0, 1, 2, 3}:
                raise InvalidSectionError(
                    f"Physical group {tag_value} has invalid dimension "
                    f"{dimension_value}"
                )
            mesh.set_physical_name(dimension_value, tag_value, name)

        expect_end_marker(io, "$EndPhysicalNames")
