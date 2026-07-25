from pathlib import Path

path = Path(".github/scripts/finalize_release_docs.py")
text = path.read_text()
old = '''    """After quality and tests succeed, a separate package job builds the wheel and
source distribution and smoke-tests the installed package and CLI.
""",
    """After quality, typing, and tests succeed, a separate package job builds the
wheel and source distribution and smoke-tests the installed package, CLI, and
packaged `py.typed` marker.
""",
'''
new = '''    """After quality and tests succeed, a separate package job builds the wheel and
source distribution and smoke-tests the installed package and CLI. The release
workflow repeats those package checks before publishing through PyPI trusted
publishing.
""",
    """After quality, typing, and tests succeed, a separate package job builds the
wheel and source distribution and smoke-tests the installed package, CLI, and
packaged `py.typed` marker. The release workflow repeats those package checks
before publishing through PyPI trusted publishing.
""",
'''
if old not in text:
    raise RuntimeError("Expected test-results transformation was not found")
path.write_text(text.replace(old, new, 1))
