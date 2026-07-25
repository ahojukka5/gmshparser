# User Guide

gmshparser has two intentionally different Python interfaces:

- `gmshparser.read()` returns the modern immutable model and is recommended for new code.
- `gmshparser.parse()` returns the original mutable compatibility model for existing applications.

Most users only need the modern interface.

## Recommended path

1. [Install gmshparser](installation.md).
2. Follow [Getting Started](getting-started.md) for a complete first read.
3. Learn the [Modern Data Model](pythonic-api.md).
4. Use [Working with Meshes](basic-usage.md) for common tasks and recipes.
5. Read [Supported Formats](supported-formats.md) before relying on optional MSH sections.

## Common tasks

| Task | Guide |
| --- | --- |
| Read a path or text stream | [Getting Started](getting-started.md) |
| Inspect nodes, elements, and entities | [Working with Meshes](basic-usage.md) |
| Resolve named boundary or material groups | [Physical Groups and Periodicity](physical-groups.md) |
| Convert topology to NumPy arrays | [NumPy Interoperability](numpy.md) |
| Handle malformed or unsupported files | [Error Handling](error-handling.md) |
| Print mesh information from a shell | [Command Line Interface](cli.md) |
| Plot 2D meshes with matplotlib | [Visualization](visualization.md) |
| Move an existing application to `read()` | [Migrating from the Compatibility API](migration.md) |

## Scope

gmshparser reads supported **ASCII** Gmsh MSH files into memory. It does not write meshes, convert formats, or retain every optional MSH section. The format guide records the exact supported versions, retained metadata, and known limitations.

For exact signatures and attributes, use the [API Reference](../api/overview.md).
