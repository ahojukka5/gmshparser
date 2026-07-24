from pathlib import Path

path = Path("gmshparser/api.py")
text = path.read_text()


def replace_once(old: str, new: str) -> None:
    global text
    count = text.count(old)
    if count != 1:
        raise RuntimeError(f"Expected one source fragment, found {count}: {old[:80]!r}")
    text = text.replace(old, new, 1)


replace_once("from enum import IntEnum\n", "")
replace_once(
    "from .main_parser import MainParser\n",
    "from .element_types import ElementFamily, ElementType, ElementTypeInfo\n"
    "from .main_parser import MainParser\n",
)
replace_once(
    '    "ElementCollection",\n    "ElementType",\n',
    '    "ElementCollection",\n    "ElementFamily",\n    "ElementType",\n'
    '    "ElementTypeInfo",\n',
)
replace_once(
    '''class ElementType(IntEnum):
    """Common numeric element types from the Gmsh MSH specification.

    Values not named here are still accepted and represented as ``TYPE_<id>``
    pseudo-members, so higher-order and future element types remain usable.
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

    @classmethod
    def _missing_(cls, value: object) -> ElementType | None:
        if not isinstance(value, int):
            return None

        member = int.__new__(cls, value)
        member._name_ = f"TYPE_{value}"
        member._value_ = value
        cls._value2member_map_[value] = member
        return member


''',
    "",
)
replace_once(
    '''    @property
    def type_id(self) -> int:
        """Raw numeric Gmsh element type."""
        return int(self.element_type)

''',
    '''    @property
    def type_id(self) -> int:
        """Raw numeric Gmsh element type."""
        return int(self.element_type)

    @property
    def info(self) -> ElementTypeInfo | None:
        """Registered topology metadata for this element type."""
        return self.element_type.info

    @property
    def family(self) -> ElementFamily | None:
        """Topological element family, or ``None`` when the type is unknown."""
        return self.element_type.family

    @property
    def order(self) -> int | None:
        """Polynomial order, or ``None`` when the type is unknown."""
        return self.element_type.order

    @property
    def expected_node_count(self) -> int | None:
        """Registered connectivity size, or ``None`` when the type is unknown."""
        return self.element_type.node_count

    @property
    def primary_node_count(self) -> int | None:
        """Number of first-order corner nodes, or ``None`` when unknown."""
        return self.element_type.primary_node_count

    @property
    def is_linear(self) -> bool:
        """Whether this is a registered first-order element."""
        return self.element_type.is_linear

    @property
    def is_high_order(self) -> bool:
        """Whether this is a registered second- or higher-order element."""
        return self.element_type.is_high_order

    @property
    def is_complete(self) -> bool | None:
        """Whether all interior high-order nodes are present, or ``None``."""
        return self.element_type.is_complete

''',
)

path.write_text(text)
