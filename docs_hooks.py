"""MkDocs hooks for keeping project landing content in one place."""

from pathlib import Path
from typing import Any


_README_IMAGE = "](docs/hero-image.webp)"
_SITE_IMAGE = "](hero-image.webp)"


def on_page_markdown(
    markdown: str,
    *,
    page: Any,
    config: Any,
    **_: Any,
) -> str:
    """Use the root README as the documentation homepage source."""
    if page.file.src_uri != "index.md":
        return markdown

    project_root = Path(config.config_file_path).resolve().parent
    readme = (project_root / "README.md").read_text(encoding="utf-8")

    # README paths are relative to the repository root. The rendered homepage
    # is rooted at docs/, where the same image is published as hero-image.webp.
    return readme.replace(_README_IMAGE, _SITE_IMAGE)
