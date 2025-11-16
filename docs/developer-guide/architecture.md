# Architecture

This document explains gmshparser's internal architecture and design decisions.

## Design Philosophy

gmshparser follows these principles:

1. **Single responsibility**: Parse Gmsh mesh files, nothing more
2. **Zero dependencies**: Pure Python, no external dependencies
3. **Extensibility**: Easy to add new parsers for new sections
4. **Version agnostic**: Same API regardless of MSH version
5. **Test-driven**: 100% test coverage goal

## System Overview

```
┌─────────────┐
│  User Code  │
└──────┬──────┘
       │ gmshparser.parse("mesh.msh")
       ▼
┌─────────────┐
│ MainParser  │ ◄─── Coordinates parsing
└──────┬──────┘
       │ Detects version
       ├─► MSH 1.0 → V1 Parsers
       ├─► MSH 2.x → V2 Parsers
       └─► MSH 4.x → V4 Parsers
       ▼
┌─────────────┐
│    Mesh     │ ◄─── Data model
└─────────────┘
```

## Core Components

### 1. Mesh Data Model

The `Mesh` class is the central data structure:

```python
class Mesh:
    - name: str
    - version: float
    - node_entities: List[NodeEntity]
    - element_entities: List[ElementEntity]
    # ... accessors and methods
```

**Node hierarchy:**

```
Mesh
  └─► NodeEntity (dimension, tag, parametric)
        └─► Node (tag, coordinates)
```

**Element hierarchy:**

```
Mesh
  └─► ElementEntity (dimension, tag, element_type)
        └─► Element (tag, connectivity)
```

### 2. Parser System

#### Abstract Parser

All parsers inherit from `AbstractParser`:

```python
class AbstractParser:
    @staticmethod
    def get_section_name() -> str:
        """Return section name like '$MeshFormat'"""
        pass
    
    @staticmethod
    def parse(mesh: Mesh, io: TextIO) -> None:
        """Parse section and populate mesh"""
        pass
```

#### Parser Registry

The `MainParser` maintains a registry of parsers:

```python
DEFAULT_PARSERS = [
    MeshFormatParser,
    NodesParser,
    ElementsParser,
]
```

When a section is encountered (e.g., `$Nodes`), `MainParser` finds the appropriate parser and delegates.

### 3. Version Manager

The `VersionManager` handles version detection and validation:

```python
class MSHVersion(Enum):
    V1_0 = 1.0
    V2_0 = 2.0
    V2_1 = 2.1
    V2_2 = 2.2
    V4_0 = 4.0
    V4_1 = 4.1
```

Functions:

- `parse_version(version_str: str) -> float`
- `is_supported(version: float) -> bool`
- `validate_version(version: float) -> None`
- `is_version_1(version: float) -> bool`
- `is_version_2(version: float) -> bool`
- `is_version_4(version: float) -> bool`

## Parsing Flow

### High-Level Flow

```
parse("mesh.msh")
    │
    ├─► Open file
    │
    ├─► Create Mesh object
    │
    ├─► MainParser.parse(mesh, file)
    │     │
    │     ├─► Detect version (first line)
    │     │
    │     ├─► Select parsers based on version
    │     │
    │     └─► For each section:
    │           └─► Find matching parser
    │               └─► Parser.parse(mesh, file)
    │
    └─► Return populated Mesh
```

### Version Detection

```python
# Read first line
line = io.readline().strip()

if line == "$MeshFormat":
    # MSH 2.x or 4.x
    version_line = io.readline().strip()
    version = float(version_line.split()[0])
elif line == "$NOD":
    # MSH 1.0 (legacy)
    version = 1.0
else:
    raise ValueError("Unknown format")
```

### Version-Specific Routing

**MSH 1.0:**

```python
parsers = [
    NodesParserV1,      # Parses $NOD section
    ElementsParserV1,   # Parses $ELM section
]
```

**MSH 2.x:**

```python
parsers = [
    MeshFormatParser,   # Parses $MeshFormat
    NodesParser,        # Parses $Nodes (V2 format)
    ElementsParser,     # Parses $Elements (V2 format)
]
```

**MSH 4.x:**

```python
parsers = [
    MeshFormatParser,   # Parses $MeshFormat
    NodesParser,        # Parses $Nodes (V4 format)
    ElementsParser,     # Parses $Elements (V4 format)
]
```

Note: MSH 4.x uses the same parser classes as MSH 2.x, but they handle the format differences internally.

## Module Structure

```
gmshparser/
├── __init__.py           # Public API: parse()
├── mesh.py               # Mesh data model
├── node.py               # Node class
├── node_entity.py        # NodeEntity class
├── element.py            # Element class
├── element_entity.py     # ElementEntity class
├── abstract_parser.py    # Parser base class
├── main_parser.py        # Main parser coordinator
├── version_manager.py    # Version detection/validation
├── mesh_format_parser.py # $MeshFormat parser
├── nodes_parser.py       # $Nodes parser (V2/V4)
├── nodes_parser_v1.py    # $NOD parser (V1)
├── nodes_parser_v2.py    # Specialized V2 $Nodes parser
├── elements_parser.py    # $Elements parser (V2/V4)
├── elements_parser_v1.py # $ELM parser (V1)
├── elements_parser_v2.py # Specialized V2 $Elements parser
├── helpers.py            # Utility functions
└── cli.py                # Command-line interface
```

## Data Flow Example

### Parsing MSH 4.1 File

```
File: mesh.msh (MSH 4.1)
    │
    ▼
$MeshFormat
4.1 0 8
$EndMeshFormat
    │
    ├─► MeshFormatParser
    │     └─► mesh.set_version(4.1)
    │
$Nodes
1 6 1 6
...
$EndNodes
    │
    ├─► NodesParser
    │     └─► Parse entity blocks
    │           └─► Create NodeEntity
    │                 └─► Add Node objects
    │
$Elements
1 2 1 2
...
$EndElements
    │
    └─► ElementsParser
          └─► Parse entity blocks
                └─► Create ElementEntity
                      └─► Add Element objects
```

## Extension Points

### Adding a New Parser

To parse a new section (e.g., `$PhysicalNames`):

1. **Create parser class:**

```python
class PhysicalNamesParser(AbstractParser):
    @staticmethod
    def get_section_name():
        return "$PhysicalNames"
    
    @staticmethod
    def parse(mesh: Mesh, io: TextIO) -> None:
        num_names = int(io.readline().strip())
        for _ in range(num_names):
            line = io.readline().strip().split()
            dimension = int(line[0])
            tag = int(line[1])
            name = " ".join(line[2:]).strip('"')
            # Store in mesh...
```

2. **Register parser:**

```python
# In main_parser.py
DEFAULT_PARSERS = [
    MeshFormatParser,
    PhysicalNamesParser,  # ← Add here
    NodesParser,
    ElementsParser,
]
```

3. **Test:**

```python
def test_physical_names_parser():
    mesh = gmshparser.parse("mesh_with_physical_names.msh")
    # Verify physical names were parsed...
```

### Adding Helper Functions

Helper functions for common operations go in `helpers.py`:

```python
def get_quads(mesh: Mesh) -> Tuple[List[float], List[float], List[List[int]]]:
    """Extract quadrilateral elements from mesh."""
    # Implementation...
```

## Performance Considerations

### Memory

- **Lazy loading**: Not implemented (all data loaded at once)
- **Memory usage**: Proportional to mesh size
- **Large meshes**: May require significant RAM

### Speed

- **File I/O**: Uses standard Python `open()`
- **Parsing**: Simple string operations
- **Bottleneck**: Usually file I/O, not parsing logic

### Optimization Opportunities

1. **Binary format support**: Faster parsing
2. **Streaming**: Parse nodes/elements on-demand
3. **Cython**: Compile performance-critical sections
4. **NumPy**: Use arrays for coordinate storage

## Testing Architecture

### Test Structure

```
tests/
├── test_mesh.py              # Mesh class
├── test_node.py              # Node class
├── test_element.py           # Element class
├── test_mesh_format_parser.py # Format parser
├── test_nodes_parser.py       # Nodes parser
├── test_elements_parser.py    # Elements parser
├── test_multi_version.py      # Version support
├── test_version_manager.py    # Version detection
├── test_helpers.py            # Helper functions
└── test_cli.py                # CLI
```

### Test Data

Located in `testdata/`:

- Simple meshes for unit tests
- Complex meshes from real-world use
- Version-specific meshes (v1.0, v2.0, v4.1, etc.)

## Design Decisions

### Why No Dependencies?

**Pros:**

- Easy installation
- No dependency conflicts
- Portable and lightweight
- Works in restricted environments

**Cons:**

- Can't use NumPy for faster array operations
- No XML parsing (if needed for newer Gmsh features)

**Decision**: Prioritize simplicity and portability.

### Why Read-Only?

**Rationale:**

- Writing MSH files is complex and error-prone
- Gmsh itself is better for mesh generation
- Parser's job is to read, not write
- Keeps codebase focused

### Why Not Support Binary Format?

**Reasons:**

- Binary format is version-specific
- Requires careful endianness handling
- ASCII is "good enough" for most use cases
- Can be added later if needed

## Future Architecture Considerations

### Potential Improvements

1. **Pluggable parsers**: Allow users to register custom parsers
2. **Streaming API**: For very large meshes
3. **Binary support**: Faster parsing
4. **Writer**: Mesh export functionality
5. **NumPy integration**: Optional NumPy arrays for coordinates

### Backward Compatibility

All public API changes will:

- Follow semantic versioning
- Maintain backward compatibility for minor versions
- Provide deprecation warnings before removal

## Related Documentation

- [Writing Parsers](writing-parsers.md)
- [Testing Guide](testing.md)
- [API Reference](../api/overview.md)
