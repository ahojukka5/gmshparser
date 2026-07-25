from pathlib import Path


def replace(path: str, old: str, new: str, *, count: int = -1) -> None:
    target = Path(path)
    text = target.read_text()
    if old not in text:
        raise RuntimeError(f"Expected text not found in {path}: {old!r}")
    target.write_text(text.replace(old, new, count))


replace(
    "gmshparser/modern_builder.py",
    "                    physical_tags=resolved_physical_tags,\n",
    "                    physical_tags=physical_tags,\n",
    count=1,
)
replace(
    "gmshparser/modern_builder.py",
    "                    physical_tags=physical_tags,\n",
    "                    physical_tags=resolved_physical_tags,\n",
    count=1,
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
