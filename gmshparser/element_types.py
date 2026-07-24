from __future__ import annotations

from dataclasses import dataclass
from enum import IntEnum, StrEnum

from .errors import (
    InvalidElementConnectivityError,
    InvalidElementError,
    UnknownElementTypeError,
)

__all__ = [
    "ElementFamily",
    "ElementType",
    "ElementTypeInfo",
    "InvalidElementConnectivityError",
    "UnknownElementTypeError",
    "require_element_type",
    "validate_element_connectivity",
    "validate_element_dimension",
]


class ElementFamily(StrEnum):
    """Topological family of a Gmsh element."""

    POINT = "point"
    LINE = "line"
    TRIANGLE = "triangle"
    QUADRANGLE = "quadrangle"
    TETRAHEDRON = "tetrahedron"
    HEXAHEDRON = "hexahedron"
    PRISM = "prism"
    PYRAMID = "pyramid"


@dataclass(frozen=True, slots=True)
class ElementTypeInfo:
    """Static topology metadata for one numeric Gmsh element type."""

    name: str
    family: ElementFamily
    dimension: int
    order: int
    node_count: int
    primary_node_count: int
    complete: bool = True

    @property
    def is_linear(self) -> bool:
        """Whether this is a first-order element."""
        return self.order == 1

    @property
    def is_high_order(self) -> bool:
        """Whether this is a second- or higher-order element."""
        return self.order > 1


class ElementType(IntEnum):
    """Numeric element types from the Gmsh MSH specification.

    Unknown numeric values remain representable as ``TYPE_<id>`` pseudo-members.
    Their topology metadata is ``None`` and parsers reject them when metadata is
    required to interpret a flat element record.
    """

    LINE = 1
    TRIANGLE = 2
    QUADRANGLE = 3
    TETRAHEDRON = 4
    HEXAHEDRON = 5
    PRISM = 6
    PYRAMID = 7
    SECOND_ORDER_LINE = 8
    SECOND_ORDER_TRIANGLE = 9
    SECOND_ORDER_QUADRANGLE = 10
    SECOND_ORDER_TETRAHEDRON = 11
    SECOND_ORDER_HEXAHEDRON = 12
    SECOND_ORDER_PRISM = 13
    SECOND_ORDER_PYRAMID = 14
    POINT = 15
    SECOND_ORDER_QUADRANGLE_INCOMPLETE = 16
    SECOND_ORDER_HEXAHEDRON_INCOMPLETE = 17
    SECOND_ORDER_PRISM_INCOMPLETE = 18
    SECOND_ORDER_PYRAMID_INCOMPLETE = 19
    THIRD_ORDER_TRIANGLE_INCOMPLETE = 20
    THIRD_ORDER_TRIANGLE = 21
    FOURTH_ORDER_TRIANGLE_INCOMPLETE = 22
    FOURTH_ORDER_TRIANGLE = 23
    FIFTH_ORDER_TRIANGLE_INCOMPLETE = 24
    FIFTH_ORDER_TRIANGLE = 25
    THIRD_ORDER_LINE = 26
    FOURTH_ORDER_LINE = 27
    FIFTH_ORDER_LINE = 28
    THIRD_ORDER_TETRAHEDRON = 29
    FOURTH_ORDER_TETRAHEDRON = 30
    FIFTH_ORDER_TETRAHEDRON = 31
    THIRD_ORDER_HEXAHEDRON = 92
    FOURTH_ORDER_HEXAHEDRON = 93

    @classmethod
    def _missing_(cls, value: object) -> ElementType | None:
        if not isinstance(value, int):
            return None

        member = int.__new__(cls, value)
        member._name_ = f"TYPE_{value}"
        member._value_ = value
        cls._value2member_map_[value] = member
        return member

    @property
    def info(self) -> ElementTypeInfo | None:
        """Registered topology metadata, or ``None`` for an unknown type."""
        return _ELEMENT_TYPE_INFO.get(int(self))

    @property
    def is_known(self) -> bool:
        """Whether topology metadata is registered for this numeric type."""
        return self.info is not None

    @property
    def family(self) -> ElementFamily | None:
        """Topological family, or ``None`` for an unknown type."""
        return None if self.info is None else self.info.family

    @property
    def dimension(self) -> int | None:
        """Topological dimension, or ``None`` for an unknown type."""
        return None if self.info is None else self.info.dimension

    @property
    def order(self) -> int | None:
        """Polynomial order, or ``None`` for an unknown type."""
        return None if self.info is None else self.info.order

    @property
    def node_count(self) -> int | None:
        """Required number of nodes, or ``None`` for an unknown type."""
        return None if self.info is None else self.info.node_count

    @property
    def primary_node_count(self) -> int | None:
        """Number of first-order corner nodes, or ``None`` when unknown."""
        return None if self.info is None else self.info.primary_node_count

    @property
    def is_complete(self) -> bool | None:
        """Whether all interior high-order nodes are present, or ``None``."""
        return None if self.info is None else self.info.complete

    @property
    def is_linear(self) -> bool:
        """Whether this is a registered first-order element."""
        return self.info is not None and self.info.is_linear

    @property
    def is_high_order(self) -> bool:
        """Whether this is a registered second- or higher-order element."""
        return self.info is not None and self.info.is_high_order


_P = ElementFamily.POINT
_L = ElementFamily.LINE
_T = ElementFamily.TRIANGLE
_Q = ElementFamily.QUADRANGLE
_TE = ElementFamily.TETRAHEDRON
_H = ElementFamily.HEXAHEDRON
_R = ElementFamily.PRISM
_Y = ElementFamily.PYRAMID

_ELEMENT_TYPE_INFO: dict[int, ElementTypeInfo] = {
    1: ElementTypeInfo("2-node line", _L, 1, 1, 2, 2),
    2: ElementTypeInfo("3-node triangle", _T, 2, 1, 3, 3),
    3: ElementTypeInfo("4-node quadrangle", _Q, 2, 1, 4, 4),
    4: ElementTypeInfo("4-node tetrahedron", _TE, 3, 1, 4, 4),
    5: ElementTypeInfo("8-node hexahedron", _H, 3, 1, 8, 8),
    6: ElementTypeInfo("6-node prism", _R, 3, 1, 6, 6),
    7: ElementTypeInfo("5-node pyramid", _Y, 3, 1, 5, 5),
    8: ElementTypeInfo("3-node second-order line", _L, 1, 2, 3, 2),
    9: ElementTypeInfo("6-node second-order triangle", _T, 2, 2, 6, 3),
    10: ElementTypeInfo("9-node second-order quadrangle", _Q, 2, 2, 9, 4),
    11: ElementTypeInfo("10-node second-order tetrahedron", _TE, 3, 2, 10, 4),
    12: ElementTypeInfo("27-node second-order hexahedron", _H, 3, 2, 27, 8),
    13: ElementTypeInfo("18-node second-order prism", _R, 3, 2, 18, 6),
    14: ElementTypeInfo("14-node second-order pyramid", _Y, 3, 2, 14, 5),
    15: ElementTypeInfo("1-node point", _P, 0, 1, 1, 1),
    16: ElementTypeInfo(
        "8-node second-order incomplete quadrangle", _Q, 2, 2, 8, 4, False
    ),
    17: ElementTypeInfo(
        "20-node second-order incomplete hexahedron", _H, 3, 2, 20, 8, False
    ),
    18: ElementTypeInfo(
        "15-node second-order incomplete prism", _R, 3, 2, 15, 6, False
    ),
    19: ElementTypeInfo(
        "13-node second-order incomplete pyramid", _Y, 3, 2, 13, 5, False
    ),
    20: ElementTypeInfo(
        "9-node third-order incomplete triangle", _T, 2, 3, 9, 3, False
    ),
    21: ElementTypeInfo("10-node third-order triangle", _T, 2, 3, 10, 3),
    22: ElementTypeInfo(
        "12-node fourth-order incomplete triangle", _T, 2, 4, 12, 3, False
    ),
    23: ElementTypeInfo("15-node fourth-order triangle", _T, 2, 4, 15, 3),
    24: ElementTypeInfo(
        "15-node fifth-order incomplete triangle", _T, 2, 5, 15, 3, False
    ),
    25: ElementTypeInfo("21-node fifth-order triangle", _T, 2, 5, 21, 3),
    26: ElementTypeInfo("4-node third-order line", _L, 1, 3, 4, 2),
    27: ElementTypeInfo("5-node fourth-order line", _L, 1, 4, 5, 2),
    28: ElementTypeInfo("6-node fifth-order line", _L, 1, 5, 6, 2),
    29: ElementTypeInfo("20-node third-order tetrahedron", _TE, 3, 3, 20, 4),
    30: ElementTypeInfo("35-node fourth-order tetrahedron", _TE, 3, 4, 35, 4),
    31: ElementTypeInfo("56-node fifth-order tetrahedron", _TE, 3, 5, 56, 4),
    92: ElementTypeInfo("64-node third-order hexahedron", _H, 3, 3, 64, 8),
    93: ElementTypeInfo("125-node fourth-order hexahedron", _H, 3, 4, 125, 8),
}


def require_element_type(value: ElementType | int) -> ElementType:
    """Return a known element type or raise a descriptive error."""
    element_type = ElementType(value)
    if element_type.info is None:
        raise UnknownElementTypeError(
            f"Unknown Gmsh element type {int(element_type)}; "
            "no topology metadata is registered"
        )
    return element_type


def validate_element_dimension(
    element_type: ElementType | int,
    dimension: int,
) -> ElementType:
    """Validate that a block dimension matches its registered element type."""
    known_type = require_element_type(element_type)
    if known_type.dimension != dimension:
        raise InvalidElementError(
            f"Element type {known_type.name} ({int(known_type)}) has dimension "
            f"{known_type.dimension}, but the element block declares {dimension}"
        )
    return known_type


def validate_element_connectivity(
    element_type: ElementType | int,
    node_tags: list[int] | tuple[int, ...],
    *,
    element_tag: int | None = None,
) -> ElementType:
    """Validate connectivity length and return the known element type."""
    known_type = require_element_type(element_type)
    expected = known_type.node_count
    actual = len(node_tags)
    if actual != expected:
        subject = "Element" if element_tag is None else f"Element {element_tag}"
        raise InvalidElementConnectivityError(
            f"{subject} of type {known_type.name} ({int(known_type)}) requires "
            f"{expected} nodes, got {actual}"
        )
    return known_type
