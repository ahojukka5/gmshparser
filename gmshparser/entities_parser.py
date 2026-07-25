from math import isfinite
from typing import TextIO

from .abstract_parser import AbstractParser
from .errors import InvalidSectionError
from .mesh import Mesh
from .parsing import expect_end_marker, read_required_line


class EntitiesParser(AbstractParser):
    """Parse MSH 4.0 and 4.1 entity records and physical assignments."""

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

        is_v40 = mesh.get_version_major() == 4 and mesh.get_version_minor() == 0
        seen_entity_tags: list[set[int]] = [set() for _ in counts]

        for dimension, count in enumerate(counts):
            geometry_count = 6 if is_v40 or dimension > 0 else 3
            physical_count_index = 1 + geometry_count

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
                    geometry = tuple(
                        float(value) for value in parts[1:physical_count_index]
                    )
                    number_of_physical_tags = int(parts[physical_count_index])
                except ValueError as error:
                    raise InvalidSectionError(
                        "Entity tags and counts must be integers and entity geometry "
                        "values must be numbers"
                    ) from error

                if tag <= 0:
                    raise InvalidSectionError("Entity tags must be positive")
                if tag in seen_entity_tags[dimension]:
                    raise InvalidSectionError(
                        f"Duplicate dimension-{dimension} entity tag {tag}"
                    )
                if any(not isfinite(value) for value in geometry):
                    raise InvalidSectionError(
                        f"Entity {tag} contains non-finite geometry values"
                    )
                if geometry_count == 6:
                    minimum = geometry[:3]
                    maximum = geometry[3:]
                    if any(
                        lower > upper
                        for lower, upper in zip(minimum, maximum, strict=True)
                    ):
                        raise InvalidSectionError(
                            f"Entity {tag} has an inverted bounding box"
                        )
                if number_of_physical_tags < 0:
                    raise InvalidSectionError(
                        "Entity physical-group counts cannot be negative"
                    )

                physical_start = physical_count_index + 1
                physical_stop = physical_start + number_of_physical_tags
                if len(parts) < physical_stop:
                    raise InvalidSectionError(
                        f"Entity {tag} declares {number_of_physical_tags} physical "
                        f"tags, but the record contains "
                        f"{max(0, len(parts) - physical_start)}"
                    )

                try:
                    physical_tags = tuple(
                        int(value) for value in parts[physical_start:physical_stop]
                    )
                except ValueError as error:
                    raise InvalidSectionError(
                        "Entity physical-group tags must be integers"
                    ) from error
                if any(physical_tag <= 0 for physical_tag in physical_tags):
                    raise InvalidSectionError(
                        "Entity physical-group tags must be positive integers"
                    )

                if dimension == 0:
                    if len(parts) != physical_stop:
                        raise InvalidSectionError(
                            f"Point entity {tag} contains unexpected trailing fields"
                        )
                else:
                    if len(parts) < physical_stop + 1:
                        raise InvalidSectionError(
                            f"Entity {tag} is missing its boundary-entity count"
                        )
                    try:
                        boundary_count = int(parts[physical_stop])
                    except ValueError as error:
                        raise InvalidSectionError(
                            "Entity boundary counts must be integers"
                        ) from error
                    if boundary_count < 0:
                        raise InvalidSectionError(
                            "Entity boundary counts cannot be negative"
                        )

                    boundary_start = physical_stop + 1
                    boundary_stop = boundary_start + boundary_count
                    if len(parts) != boundary_stop:
                        available = max(0, len(parts) - boundary_start)
                        raise InvalidSectionError(
                            f"Entity {tag} declares {boundary_count} boundary tags, "
                            f"but the record contains {available}"
                        )
                    try:
                        boundary_tags = tuple(
                            int(value) for value in parts[boundary_start:boundary_stop]
                        )
                    except ValueError as error:
                        raise InvalidSectionError(
                            "Entity boundary tags must be integers"
                        ) from error
                    if any(boundary_tag == 0 for boundary_tag in boundary_tags):
                        raise InvalidSectionError(
                            "Entity boundary tags must be non-zero signed integers"
                        )

                seen_entity_tags[dimension].add(tag)
                mesh.set_entity_physical_tags(dimension, tag, physical_tags)

        expect_end_marker(io, "$EndEntities")
