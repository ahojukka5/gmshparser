# Test Data

This directory contains ASCII Gmsh MSH files used by the automated tests and
manual examples.

## Organization

- `simple/` contains small, purpose-built meshes for version and parser tests.
- `complex/` contains larger or externally sourced regression cases and their
  attribution notes.
- `large/` contains the larger example mesh used by visualization and
  performance-oriented checks.

The repository currently stores these files directly in Git. Git LFS is not
configured.

## Supported-version fixtures

The simple fixtures cover the supported format families, including MSH 1.0,
MSH 2.x, and MSH 4.x. Tests should refer to the exact committed filename rather
than assuming a generated file is available.

## Adding a mesh

Prefer the smallest file that reproduces the behavior under test.

1. Place a small synthetic fixture in `simple/`.
2. Place a real-world or multi-feature regression case in a suitable
   `complex/` subdirectory.
3. Include the source `.geo` file when it is available and useful.
4. Add attribution and licensing information for externally sourced data.
5. Add a focused pytest test that states the expected version, counts, or
   parser behavior.

Example:

```python
import gmshparser


def test_contributed_mesh():
    mesh = gmshparser.parse("testdata/complex/example.msh")

    assert mesh.get_version() == 4.1
    assert mesh.get_number_of_nodes() > 0
    assert mesh.get_number_of_elements() > 0
```

Do not document invented counts or files before they are committed and tested.

## Large files

Avoid adding unnecessarily large meshes. If future fixtures become large enough
to justify Git LFS, configure `.gitattributes` in the same change and update this
README. Until then, do not describe files as LFS-managed.

## External data

A contributed mesh must be redistributable under terms compatible with this
repository. Record its source and any required attribution in a README next to
the file.

## Running tests

```bash
uv sync
uv run pytest
```

See [Test Results](../docs/developer-guide/test-results.md) for the current CI
matrix and [Testing Guide](../docs/developer-guide/testing.md) for development
commands.
