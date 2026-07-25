from pathlib import Path


def replace(path: str, old: str, new: str, *, count: int = -1) -> None:
    target = Path(path)
    text = target.read_text()
    if old not in text:
        raise RuntimeError(f"Expected text not found in {path}: {old!r}")
    target.write_text(text.replace(old, new, count))


for path in (
    "gmshparser/physical_names_parser.py",
    "gmshparser/nodes_parser_v2.py",
    "gmshparser/nodes_parser_v1.py",
    "gmshparser/nodes_parser.py",
    "gmshparser/mesh_format_parser.py",
    "gmshparser/entities_parser.py",
    "gmshparser/elements_parser_v2.py",
    "gmshparser/elements_parser_v1.py",
    "gmshparser/elements_parser.py",
):
    replace(path, "def get_section_name():", "def get_section_name() -> str:")

replace(
    "gmshparser/modern_builder.py",
    "from typing import TYPE_CHECKING\n",
    "from collections.abc import Iterable\nfrom typing import TYPE_CHECKING\n",
)
replace(
    "gmshparser/modern_builder.py",
    "type RawElementBlock = tuple[int, int, int, list[RawElement]]\n",
    """type RawElementBlock = tuple[int, int, int, list[RawElement]]
type NodePair = tuple[int, int]
type PeriodicLinkValue = tuple[int, tuple[float, ...], tuple[NodePair, ...]]
type PeriodicLinkRecord = tuple[
    int,
    int,
    int,
    tuple[float, ...],
    tuple[NodePair, ...],
]
""",
)
replace(
    "gmshparser/modern_builder.py",
    "    def __init__(self, name: str = \"New Mesh\"):\n",
    "    def __init__(self, name: str = \"New Mesh\") -> None:\n",
)
replace(
    "gmshparser/modern_builder.py",
    """        nodes,
    ) -> None:
""",
    """        nodes: Iterable[RawNode],
    ) -> None:
""",
    count=1,
)
replace(
    "gmshparser/modern_builder.py",
    """        elements,
    ) -> None:
""",
    """        elements: Iterable[RawElement],
    ) -> None:
""",
    count=1,
)
replace(
    "gmshparser/modern_builder.py",
    """        physical_tags,
    ) -> None:
""",
    """        physical_tags: Iterable[int],
    ) -> None:
""",
    count=1,
)
replace(
    "gmshparser/modern_builder.py",
    """        physical_tags,
    ) -> None:
""",
    """        physical_tags: Iterable[int],
    ) -> None:
""",
    count=1,
)
replace(
    "gmshparser/modern_builder.py",
    "    def set_element_physical_tags(self, element_tag: int, physical_tags) -> None:\n",
    """    def set_element_physical_tags(
        self,
        element_tag: int,
        physical_tags: Iterable[int],
    ) -> None:
""",
)
replace(
    "gmshparser/modern_builder.py",
    """        affine_transform,
        node_pairs,
    ) -> None:
""",
    """        affine_transform: Iterable[float],
        node_pairs: Iterable[NodePair],
    ) -> None:
""",
)
replace(
    "gmshparser/modern_builder.py",
    "    def get_periodic_link(self, dimension: int, entity_tag: int):\n",
    """    def get_periodic_link(
        self,
        dimension: int,
        entity_tag: int,
    ) -> PeriodicLinkValue:
""",
)
replace(
    "gmshparser/modern_builder.py",
    "    def get_periodic_links(self):\n",
    "    def get_periodic_links(self) -> tuple[PeriodicLinkRecord, ...]:\n",
)
replace(
    "gmshparser/modern_builder.py",
    "    def _normalize_tags(tags) -> tuple[int, ...]:\n",
    "    def _normalize_tags(tags: Iterable[int]) -> tuple[int, ...]:\n",
)
