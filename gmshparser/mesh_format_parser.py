from typing import TextIO

from .abstract_parser import AbstractParser
from .errors import (
    InvalidSectionError,
    UnsupportedBinaryFormatError,
    UnsupportedVersionError,
)
from .mesh import Mesh
from .parsing import expect_end_marker, read_required_line
from .version_manager import VersionManager


class MeshFormatParser(AbstractParser):
    """Parse and validate the ``$MeshFormat`` section."""

    @staticmethod
    def get_section_name() -> str:
        return "$MeshFormat"

    @staticmethod
    def parse(mesh: Mesh, io: TextIO) -> None:
        line = read_required_line(io, "$MeshFormat header")
        fields = line.strip().split()
        if len(fields) != 3:
            raise InvalidSectionError(
                "$MeshFormat header must contain version, file type, and data size"
            )

        try:
            version_enum = VersionManager.validate_version(fields[0])
        except ValueError as error:
            raise UnsupportedVersionError(str(error)) from error

        try:
            file_type = int(fields[1])
            data_size = int(fields[2])
        except ValueError as error:
            raise InvalidSectionError(
                "$MeshFormat file type and data size must be integers"
            ) from error

        if file_type not in {0, 1}:
            raise InvalidSectionError(
                f"Unsupported $MeshFormat file type {file_type}; expected 0 or 1"
            )
        if file_type == 1:
            raise UnsupportedBinaryFormatError(
                "Binary MSH files are not supported; provide an ASCII MSH file"
            )
        if data_size <= 0:
            raise InvalidSectionError("$MeshFormat data size must be positive")

        mesh.set_version(version_enum.version_number)
        mesh.set_ascii(True)
        mesh.set_precision(data_size)
        expect_end_marker(io, "$EndMeshFormat")
