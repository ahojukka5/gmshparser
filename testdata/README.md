# Test Data

This directory contains mesh files used for testing gmshparser across different MSH format versions.

## Directory Structure

```
testdata/
├── README.md           # This file
├── simple/            # Simple test meshes for unit tests
├── complex/           # Complex meshes with mixed elements
└── large/             # Large meshes (Git LFS)
```

## File Organization

### simple/

Small, straightforward meshes for basic testing:

- `testmesh_v1_0.msh` - MSH 1.0 format, 6 nodes, 2 quads
- `testmesh_v2_0.msh` - MSH 2.0 format, 6 nodes, 2 quads
- `testmesh_v2_1.msh` - MSH 2.1 format with physical groups
- `testmesh.msh` - MSH 4.1 format, 6 nodes, 2 quads

### complex/

Meshes with multiple element types and features:

- `complex_v1_0.msh` - MSH 1.0 with points, lines, triangles, quads, tets
- `mixed_v2_0.msh` - MSH 2.0 with mixed 2D elements
- `physical_v2_1.msh` - MSH 2.1 with physical group metadata
- `entities_v4_1.msh` - MSH 4.1 demonstrating entity structure

### large/

Large meshes for performance testing (stored with Git LFS):

- `example_mesh.msh` - MSH 4.1, 197 nodes, 396 triangular elements

## Contributing Test Data

We welcome contributions of mesh files! If you have interesting test cases:

### What We Need

- **Various MSH versions**: Especially edge cases in different versions
- **Different element types**: High-order elements, 3D elements, mixed meshes
- **Real-world examples**: Actual meshes from FEM simulations
- **Edge cases**: Unusual geometries, boundary conditions

### How to Contribute

1. **For small files** (< 1 MB):

   ```bash
   # Add file to appropriate directory
   cp your_mesh.msh testdata/simple/  # or complex/
   
   # Commit and push
   git add testdata/simple/your_mesh.msh
   git commit -m "Add test mesh: your_mesh.msh"
   ```

2. **For large files** (> 1 MB):

   Large files should use Git LFS to avoid bloating the repository.

   ```bash
   # Install Git LFS (if not already installed)
   git lfs install
   
   # Track large mesh files
   git lfs track "testdata/large/*.msh"
   
   # Add .gitattributes
   git add .gitattributes
   
   # Add your large mesh file
   cp your_large_mesh.msh testdata/large/
   git add testdata/large/your_large_mesh.msh
   
   # Commit and push
   git commit -m "Add large test mesh: your_large_mesh.msh"
   git push
   ```

### Include .geo Files

If you have the Gmsh `.geo` files used to generate the meshes, please include them:

```bash
cp mesh.geo testdata/simple/
git add testdata/simple/mesh.geo
git commit -m "Add .geo file for test mesh"
```

This helps others understand how the mesh was created and regenerate it if needed.

## File Naming Convention

Use descriptive names that indicate:

1. **Purpose**: `simple_`, `complex_`, `large_`
2. **Format version**: `_v1_0`, `_v2_0`, `_v4_1`
3. **Features**: `_mixed`, `_physical`, `_periodic`

Examples:

- `simple_quad_v2_0.msh`
- `complex_mixed_3d_v4_1.msh`
- `large_structural_mesh_v4_1.msh`

## Git LFS Setup

If you plan to add large files, set up Git LFS:

### Installation

**Linux:**

```bash
sudo apt-get install git-lfs  # Debian/Ubuntu
sudo dnf install git-lfs      # Fedora
```

**macOS:**

```bash
brew install git-lfs
```

**Windows:**

Download from [git-lfs.github.com](https://git-lfs.github.com/)

### Initialize

```bash
cd /path/to/gmshparser
git lfs install
git lfs track "testdata/large/*.msh"
git add .gitattributes
git commit -m "Configure Git LFS for large mesh files"
```

### Verify

```bash
# Check tracked patterns
git lfs track

# Check LFS status
git lfs status
```

## Testing Your Mesh

After adding a mesh file, verify it works:

```python
import gmshparser

# Parse your mesh
mesh = gmshparser.parse("testdata/simple/your_mesh.msh")

# Check basic properties
print(f"Version: {mesh.get_version()}")
print(f"Nodes: {mesh.get_number_of_nodes()}")
print(f"Elements: {mesh.get_number_of_elements()}")

# Verify it parses correctly
assert mesh.get_number_of_nodes() > 0
assert mesh.get_number_of_elements() > 0
```

Add a test case:

```python
# In tests/test_contributed_meshes.py
def test_your_mesh():
    """Test parsing your_mesh.msh"""
    mesh = gmshparser.parse("testdata/simple/your_mesh.msh")
    assert mesh.get_version() == 4.1
    assert mesh.get_number_of_nodes() == 42
    assert mesh.get_number_of_elements() == 80
```

## License and Attribution

By contributing mesh files, you agree that:

1. You have the right to contribute the file
2. The file can be used under the project's MIT license
3. The file can be redistributed with gmshparser

If your mesh file requires attribution, add details to this README:

### Attributions

- `example_mesh.msh` - Created by Jukka Aho for testing purposes
- `your_mesh.msh` - Contributed by Your Name, description of origin

## Current Test Coverage

See [Test Results](../docs/developer-guide/test-results.md) for details on which formats and features are currently tested.

## Questions?

If you have questions about contributing test data:

- Open a [GitHub issue](https://github.com/ahojukka5/gmshparser/issues)
- Contact: <ahojukka5@gmail.com>

Thank you for helping improve gmshparser! 🎉
