from pathlib import Path


def replace_once(path: Path, old: str, new: str) -> None:
    text = path.read_text()
    count = text.count(old)
    if count != 1:
        raise RuntimeError(
            f"Expected one source fragment in {path}, found {count}: {old[:80]!r}"
        )
    path.write_text(text.replace(old, new, 1))


replace_once(
    Path("docs/user-guide/pythonic-api.md"),
    """Unnamed higher-order or future values remain usable as `TYPE_<id>` enum
pseudo-members.
""",
    """The element type registry exposes topology metadata without separate lookup
tables:

```python
kind = ElementType.SECOND_ORDER_TRIANGLE

print(kind.family)              # triangle
print(kind.dimension)           # 2
print(kind.order)               # 2
print(kind.node_count)          # 6
print(kind.primary_node_count)  # 3
print(kind.is_linear)           # False
print(kind.is_high_order)       # True
print(kind.is_complete)         # True
```

The same information is available directly from an element through
`element.info`, `element.family`, `element.order`, `element.expected_node_count`,
`element.primary_node_count`, `element.is_linear`, `element.is_high_order`, and
`element.is_complete`.

Unknown numeric values remain usable as `TYPE_<id>` enum pseudo-members, with
metadata properties set to `None`. Parsers reject types whose topology is needed
but unknown instead of silently guessing their dimension.
""",
)

replace_once(
    Path("docs/about/changelog.md"),
    """- descriptive `ElementType` integer enum with support for unnamed numeric types
""",
    """- centralized element type registry for numeric IDs 1–31 and 92–93 with
  family, dimension, polynomial order, connectivity size, primary-node count,
  and complete/incomplete metadata
- descriptive `ElementType` integer enum that keeps unknown numeric values
  representable without silently inferring their topology
""",
)

replace_once(
    Path("docs/about/changelog.md"),
    """- made `Element.element_type` the canonical modern attribute while retaining
  `Element.type` as an alias
""",
    """- made `Element.element_type` the canonical modern attribute while retaining
  `Element.type` as an alias
- unified MSH 1.x, 2.x, and 4.x dimension and connectivity validation around the
  centralized element registry
""",
)
