from pathlib import Path


def replace(path: str, old: str, new: str) -> None:
    target = Path(path)
    text = target.read_text()
    if old not in text:
        raise RuntimeError(f"Expected text not found in {path}: {old!r}")
    target.write_text(text.replace(old, new, 1))


replace(
    "gmshparser/modern_builder.py",
    """                    parametric_coordinates=coordinates[3:],
                    physical_tags=resolved_physical_tags,
""",
    """                    parametric_coordinates=coordinates[3:],
                    physical_tags=physical_tags,
""",
)
replace(
    "gmshparser/modern_builder.py",
    """                    dimension=dimension,
                    entity_tag=entity_tag,
                    physical_tags=physical_tags,
""",
    """                    dimension=dimension,
                    entity_tag=entity_tag,
                    physical_tags=resolved_physical_tags,
""",
)
replace(
    "gmshparser/api.py",
    """class _Tagged(Protocol):
    tag: int
""",
    """class _Tagged(Protocol):
    @property
    def tag(self) -> int: ...
""",
)
