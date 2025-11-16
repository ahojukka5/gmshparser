# Test Mesh Files from Internet

This directory contains comprehensive test mesh files covering different MSH format versions and features.

## Files Overview

### MSH 1.0 Format

- `complex_v1_0.msh` - Complex mesh with 12 nodes, 14 elements including:
  - Point elements (type 15)
  - Line elements (type 1)
  - Triangle elements (type 2)
  - Quadrangle elements (type 3)
  - Tetrahedron elements (type 4)

### MSH 2.0 Format

- `mixed_v2_0.msh` - Mixed 2D mesh with 8 nodes, 7 elements:
  - Point elements (type 15)
  - Line elements (type 1)
  - Triangle elements (type 2)
  - Quadrangle elements (type 3)

### MSH 2.1 Format

- `physical_v2_1.msh` - Mesh with physical groups:
  - Includes $PhysicalNames section
  - 10 nodes, 12 elements
  - Physical groups: "LeftEdge" (1D), "Surface1" (2D), "Volume1" (3D)
  - Point, line, triangle, and tetrahedron elements

### MSH 4.1 Format

- `entities_v4_1.msh` - Modern format with $Entities section:
  - Entity-based organization
  - 6 nodes, 2 elements
  - Quadrangle elements

## Test Results

All files successfully parse with gmshparser supporting:

- **MSH 1.0**: Legacy format with $NOD/$ENDNOD and $ELM/$ENDELM sections
- **MSH 2.0**: Standard format with $MeshFormat, $Nodes, $Elements sections
- **MSH 2.1**: Extends 2.0 with $PhysicalNames support
- **MSH 2.2**: Compatible with 2.0/2.1 parsers (same structure)
- **MSH 4.0/4.1**: Modern format with $Entities section for topology

## Validation

Run the test suite:

```bash
python3 -c "
import gmshparser
import glob

for f in glob.glob('data/test_from_internet/*.msh'):
    mesh = gmshparser.parse(f)
    print(f'{f}: v{mesh.get_version()}, {mesh.get_number_of_nodes()} nodes, {mesh.get_number_of_elements()} elements')
"
```

All meshes should parse without errors, demonstrating compatibility across all supported MSH format versions.
