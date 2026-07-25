from __future__ import annotations

from typing import TextIO

from .abstract_parser import AbstractParser
from .errors import InvalidSectionError
from .mesh import Mesh
from .parsing import expect_end_marker, read_required_line


class PeriodicParser(AbstractParser):
    """Parse periodic entity and node correspondences from MSH 2.x and 4.x."""

    @staticmethod
    def get_section_name() -> str:
        return "$Periodic"

    @staticmethod
    def parse(mesh: Mesh, io: TextIO) -> None:
        line = read_required_line(io, "$Periodic count")
        if line.strip() == "$Periodic":
            line = read_required_line(io, "$Periodic count")
        link_count = _parse_count(line, "$Periodic link count")

        major = mesh.get_version_major()
        is_v40 = major == 4 and mesh.get_version_minor() == 0

        for _ in range(link_count):
            relation = _parse_int_fields(
                read_required_line(io, "a periodic entity relation"),
                "A periodic entity relation",
                expected=3,
            )
            dimension, entity_tag, master_entity_tag = relation
            if dimension not in {0, 1, 2, 3}:
                raise InvalidSectionError(
                    f"Periodic entity {entity_tag} has invalid dimension {dimension}"
                )
            if entity_tag <= 0 or master_entity_tag <= 0:
                raise InvalidSectionError("Periodic entity tags must be positive")
            if mesh.has_periodic_link(dimension, entity_tag):
                raise InvalidSectionError(
                    f"Duplicate periodic link for entity ({dimension}, {entity_tag})"
                )

            next_line = read_required_line(io, "periodic affine data or node count")
            if major == 2 or is_v40:
                affine_transform, node_count_line = _parse_optional_affine(
                    io, next_line
                )
            else:
                affine_transform = _parse_counted_affine(io, next_line)
                node_count_line = read_required_line(
                    io, "periodic corresponding-node count"
                )

            node_count = _parse_count(
                node_count_line, "Periodic corresponding-node count"
            )
            node_pairs: list[tuple[int, int]] = []
            seen_slave_tags: set[int] = set()
            for _ in range(node_count):
                slave_tag, master_tag = _parse_int_fields(
                    read_required_line(io, "a periodic node correspondence"),
                    "A periodic node correspondence",
                    expected=2,
                )
                if slave_tag <= 0 or master_tag <= 0:
                    raise InvalidSectionError("Periodic node tags must be positive")
                if slave_tag in seen_slave_tags:
                    raise InvalidSectionError(
                        f"Duplicate periodic slave node tag {slave_tag}"
                    )
                seen_slave_tags.add(slave_tag)
                node_pairs.append((slave_tag, master_tag))

            mesh.add_periodic_link(
                dimension,
                entity_tag,
                master_entity_tag,
                affine_transform,
                node_pairs,
            )

        expect_end_marker(io, "$EndPeriodic")


def _parse_optional_affine(io: TextIO, line: str) -> tuple[tuple[float, ...], str]:
    """Parse the optional ``Affine ...`` record used by MSH 2.x and 4.0."""
    fields = line.strip().split()
    if not fields or fields[0] != "Affine":
        return (), line
    try:
        values = tuple(float(value) for value in fields[1:])
    except ValueError as error:
        raise InvalidSectionError("Periodic affine values must be numbers") from error
    return values, read_required_line(io, "periodic corresponding-node count")


def _parse_counted_affine(io: TextIO, line: str) -> tuple[float, ...]:
    """Parse the count-prefixed affine record introduced in MSH 4.1."""
    fields = line.strip().split()
    if not fields:
        raise InvalidSectionError("Periodic affine record cannot be empty")
    try:
        count = int(fields[0])
    except ValueError as error:
        raise InvalidSectionError(
            "Periodic affine record must begin with an integer count"
        ) from error
    if count < 0:
        raise InvalidSectionError("Periodic affine count cannot be negative")

    raw_values = fields[1:]
    while len(raw_values) < count:
        continuation = read_required_line(io, "periodic affine values").strip()
        if continuation.startswith("$"):
            raise InvalidSectionError(
                f"Periodic affine record declares {count} values, got {len(raw_values)}"
            )
        raw_values.extend(continuation.split())
    if len(raw_values) != count:
        raise InvalidSectionError(
            f"Periodic affine record declares {count} values, got {len(raw_values)}"
        )
    try:
        return tuple(float(value) for value in raw_values)
    except ValueError as error:
        raise InvalidSectionError("Periodic affine values must be numbers") from error


def _parse_count(line: str, description: str) -> int:
    fields = line.strip().split()
    if len(fields) != 1:
        raise InvalidSectionError(f"{description} must contain one integer")
    try:
        count = int(fields[0])
    except ValueError as error:
        raise InvalidSectionError(f"{description} must be an integer") from error
    if count < 0:
        raise InvalidSectionError(f"{description} cannot be negative")
    return count


def _parse_int_fields(
    line: str,
    description: str,
    *,
    expected: int,
) -> tuple[int, ...]:
    fields = line.strip().split()
    if len(fields) != expected:
        raise InvalidSectionError(
            f"{description} must contain exactly {expected} integers"
        )
    try:
        return tuple(int(value) for value in fields)
    except ValueError as error:
        raise InvalidSectionError(f"{description} must contain integers") from error
