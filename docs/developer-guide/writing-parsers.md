# Writing Custom Parsers

gmshparser's modular architecture makes it easy to add custom parsers for new mesh file sections.

## Parser Basics

Every parser must:

1. Inherit from `AbstractParser`
2. Implement `get_section_name()` - returns the section identifier (e.g., `"$PhysicalNames"`)
3. Implement `parse(mesh, io)` - reads from file and populates mesh

## Simple Example

Here's a parser for the `$PhysicalNames` section:

```python
from gmshparser.abstract_parser import AbstractParser
from gmshparser.mesh import Mesh
from typing import TextIO

class PhysicalNamesParser(AbstractParser):
    """Parser for $PhysicalNames section."""
    
    @staticmethod
    def get_section_name() -> str:
        return "$PhysicalNames"
    
    @staticmethod
    def parse(mesh: Mesh, io: TextIO) -> None:
        """Parse physical names from mesh file.
        
        Format:
            $PhysicalNames
            <num_names>
            <dimension> <physical_tag> "<name>"
            ...
            $EndPhysicalNames
        """
        # Read number of physical names
        num_names = int(io.readline().strip())
        
        # Parse each physical name
        physical_names = {}
        for _ in range(num_names):
            line = io.readline().strip().split(maxsplit=2)
            dimension = int(line[0])
            tag = int(line[1])
            name = line[2].strip('"')
            physical_names[(dimension, tag)] = name
        
        # Store in mesh (you'd need to add this method to Mesh)
        mesh.set_physical_names(physical_names)
```

## Registering Your Parser

Add your parser to the parser registry:

```python
# In main_parser.py
from gmshparser.physical_names_parser import PhysicalNamesParser

DEFAULT_PARSERS = [
    MeshFormatParser,
    PhysicalNamesParser,  # Your custom parser
    NodesParser,
    ElementsParser,
]
```

## Testing Your Parser

Create comprehensive tests:

```python
# tests/test_physical_names_parser.py
import gmshparser

def test_physical_names_parser():
    """Test PhysicalNames parser."""
    mesh = gmshparser.parse("testdata/physical_names.msh")
    
    names = mesh.get_physical_names()
    assert (2, 1) in names
    assert names[(2, 1)] == "Surface1"
```

## Advanced Example: Periodic Entities

For more complex sections:

```python
class PeriodicParser(AbstractParser):
    """Parser for $Periodic section (MSH 4.x)."""
    
    @staticmethod
    def get_section_name() -> str:
        return "$Periodic"
    
    @staticmethod
    def parse(mesh: Mesh, io: TextIO) -> None:
        """Parse periodic entity information."""
        num_periodic = int(io.readline().strip())
        
        periodic_entities = []
        for _ in range(num_periodic):
            line = io.readline().strip().split()
            dimension = int(line[0])
            slave_tag = int(line[1])
            master_tag = int(line[2])
            
            # Read transformation matrix (if present)
            if len(line) > 3:
                num_values = int(line[3])
                transform = [float(io.readline().strip()) for _ in range(num_values)]
            else:
                transform = None
            
            periodic_entities.append({
                'dimension': dimension,
                'slave': slave_tag,
                'master': master_tag,
                'transform': transform
            })
        
        mesh.set_periodic_entities(periodic_entities)
```

## Best Practices

### 1. Error Handling

```python
def parse(mesh: Mesh, io: TextIO) -> None:
    try:
        num_items = int(io.readline().strip())
    except ValueError as e:
        raise ValueError(f"Invalid format in $Section: {e}")
    
    if num_items < 0:
        raise ValueError(f"Invalid count: {num_items}")
```

### 2. Type Hints

```python
from typing import TextIO, List, Dict

def parse(mesh: Mesh, io: TextIO) -> None:
    data: Dict[int, List[float]] = {}
    # ...
```

### 3. Documentation

```python
def parse(mesh: Mesh, io: TextIO) -> None:
    """Parse section from mesh file.
    
    Args:
        mesh: Mesh object to populate
        io: File handle positioned after section header
    
    Raises:
        ValueError: If section format is invalid
    
    Example:
        Format in file:
            $SectionName
            <data>
            $EndSectionName
    """
```

### 4. Don't Read the End Marker

The `MainParser` handles `$End*` markers. Your parser should stop before it:

```python
# ✅ Correct
def parse(mesh: Mesh, io: TextIO) -> None:
    count = int(io.readline())
    for _ in range(count):
        line = io.readline()
        # Process line
    # Stop here - don't read $EndSection

# ❌ Incorrect
def parse(mesh: Mesh, io: TextIO) -> None:
    count = int(io.readline())
    for _ in range(count):
        line = io.readline()
    end_marker = io.readline()  # Don't do this!
```

## Version-Specific Parsers

For sections that differ between versions, use version checks:

```python
def parse(mesh: Mesh, io: TextIO) -> None:
    version = mesh.get_version()
    
    if version < 2.0:
        parse_v1_format(mesh, io)
    elif version < 4.0:
        parse_v2_format(mesh, io)
    else:
        parse_v4_format(mesh, io)
```

Or create separate parser classes:

```python
class NodeDataParserV2(AbstractParser):
    @staticmethod
    def get_section_name() -> str:
        return "$NodeData"
    
    @staticmethod
    def parse(mesh: Mesh, io: TextIO) -> None:
        # V2 format parsing
        pass

class NodeDataParserV4(AbstractParser):
    @staticmethod
    def get_section_name() -> str:
        return "$NodeData"
    
    @staticmethod
    def parse(mesh: Mesh, io: TextIO) -> None:
        # V4 format parsing
        pass
```

## Modifying the Mesh Class

If your parser needs to store new data:

```python
# In mesh.py
class Mesh:
    def __init__(self):
        # ... existing fields
        self._physical_names = {}
    
    def set_physical_names(self, names: Dict[Tuple[int, int], str]) -> None:
        """Set physical group names."""
        self._physical_names = names
    
    def get_physical_names(self) -> Dict[Tuple[int, int], str]:
        """Get physical group names."""
        return self._physical_names
    
    def get_physical_name(self, dimension: int, tag: int) -> str:
        """Get physical name by dimension and tag."""
        return self._physical_names.get((dimension, tag), "")
```

## Complete Example: NodeData Parser

```python
from gmshparser.abstract_parser import AbstractParser
from gmshparser.mesh import Mesh
from typing import TextIO, List, Dict

class NodeDataParser(AbstractParser):
    """Parser for $NodeData section (post-processing data)."""
    
    @staticmethod
    def get_section_name() -> str:
        return "$NodeData"
    
    @staticmethod
    def parse(mesh: Mesh, io: TextIO) -> None:
        """Parse node data for visualization.
        
        Format (MSH 2.x):
            $NodeData
            <num_string_tags>
            "<view_name>"
            <num_real_tags>
            <time_value>
            <num_integer_tags>
            <time_step>
            <num_components>
            <num_nodes>
            <node_tag> <value1> [<value2> ...]
            ...
            $EndNodeData
        """
        # String tags
        num_string_tags = int(io.readline().strip())
        string_tags = [io.readline().strip().strip('"') for _ in range(num_string_tags)]
        view_name = string_tags[0] if string_tags else "Unnamed"
        
        # Real tags
        num_real_tags = int(io.readline().strip())
        real_tags = [float(io.readline().strip()) for _ in range(num_real_tags)]
        time_value = real_tags[0] if real_tags else 0.0
        
        # Integer tags
        num_integer_tags = int(io.readline().strip())
        integer_tags = [int(io.readline().strip()) for _ in range(num_integer_tags)]
        time_step = integer_tags[0] if len(integer_tags) > 0 else 0
        num_components = integer_tags[1] if len(integer_tags) > 1 else 1
        num_nodes = integer_tags[2] if len(integer_tags) > 2 else 0
        
        # Node data
        node_data: Dict[int, List[float]] = {}
        for _ in range(num_nodes):
            parts = io.readline().strip().split()
            node_tag = int(parts[0])
            values = [float(v) for v in parts[1:]]
            node_data[node_tag] = values
        
        # Store in mesh
        mesh.add_node_data(view_name, {
            'time': time_value,
            'time_step': time_step,
            'components': num_components,
            'data': node_data
        })
```

## Debugging Tips

### 1. Print Debug Info

```python
def parse(mesh: Mesh, io: TextIO) -> None:
    position = io.tell()
    print(f"Parsing at position {position}")
    line = io.readline()
    print(f"Read line: {line}")
```

### 2. Validate Input

```python
def parse(mesh: Mesh, io: TextIO) -> None:
    line = io.readline().strip()
    parts = line.split()
    
    if len(parts) < 3:
        raise ValueError(f"Expected at least 3 values, got {len(parts)}: {line}")
```

### 3. Test with Simple Files

Create minimal test files:

```text
$MeshFormat
4.1 0 8
$EndMeshFormat
$YourSection
1
test data
$EndYourSection
```

## Contributing Your Parser

If you've written a useful parser:

1. Add tests
2. Update documentation
3. Submit a pull request

See [Contributing Guide](contributing.md) for details.

## Next Steps

- Review [Architecture](architecture.md) for system overview
- Check [Testing Guide](testing.md) for test practices
- See [API Reference](../api/parsers.md) for existing parsers
