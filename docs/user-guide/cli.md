# Command Line Interface

gmshparser includes a command-line interface (CLI) for quick mesh inspection and data extraction without writing Python code.

## Basic Usage

After installing gmshparser, the `gmshparser` command is available in your terminal:

```bash
gmshparser <mesh_file> <command>
```

## Available Commands

### `nodes` - Extract Node Data

Extract all nodes in a simple format:

```bash
gmshparser mesh.msh nodes
```

**Output format:**

```text
<number_of_nodes>
<node_id> <x> <y> <z>
<node_id> <x> <y> <z>
...
```

**Example:**

```bash
$ gmshparser data/testmesh.msh nodes
6
1 0.000000 0.000000 0.000000
2 1.000000 0.000000 0.000000
3 1.000000 1.000000 0.000000
4 0.000000 1.000000 0.000000
5 2.000000 0.000000 0.000000
6 2.000000 1.000000 0.000000
```

### `elements` - Extract Element Data

Extract all elements with their connectivity:

```bash
gmshparser mesh.msh elements
```

**Output format:**

```text
<number_of_elements>
<element_id> <element_type> <node_1> <node_2> ... <node_n>
<element_id> <element_type> <node_1> <node_2> ... <node_n>
...
```

**Example:**

```bash
$ gmshparser data/testmesh.msh elements
2
1 3 1 2 3 4
2 3 2 5 6 3
```

## Practical Use Cases

### 1. Quick Mesh Inspection

Check mesh contents without writing code:

```bash
# Count nodes
gmshparser mesh.msh nodes | wc -l

# Count elements
gmshparser mesh.msh elements | wc -l

# View first 10 nodes
gmshparser mesh.msh nodes | head -n 11
```

### 2. Import to Other Languages

The simple output format makes it easy to read mesh data in C, C++, Fortran, or other languages:

**C++ Example:**

```cpp
#include <iostream>
#include <fstream>

int main() {
    std::ifstream nodes("nodes.txt");
    int num_nodes;
    nodes >> num_nodes;
    
    for (int i = 0; i < num_nodes; ++i) {
        int id;
        double x, y, z;
        nodes >> id >> x >> y >> z;
        std::cout << "Node " << id << ": (" << x << ", " << y << ", " << z << ")\n";
    }
    
    return 0;
}
```

**Fortran Example:**

```fortran
program read_mesh
    implicit none
    integer :: num_nodes, i, node_id
    real(8) :: x, y, z
    
    open(unit=10, file='nodes.txt', status='old')
    read(10, *) num_nodes
    
    do i = 1, num_nodes
        read(10, *) node_id, x, y, z
        write(*, '(A,I0,A,3F12.6)') 'Node ', node_id, ': ', x, y, z
    end do
    
    close(10)
end program read_mesh
```

### 3. Pipeline Processing

Combine with shell tools for data processing:

```bash
# Extract nodes and save to file
gmshparser mesh.msh nodes > nodes.txt

# Extract elements and save to file
gmshparser mesh.msh elements > elements.txt

# Extract only node coordinates (skip IDs)
gmshparser mesh.msh nodes | tail -n +2 | awk '{print $2, $3, $4}'

# Count triangular elements (type 2)
gmshparser mesh.msh elements | grep "^[0-9]* 2 " | wc -l
```

### 4. Batch Processing

Process multiple meshes:

```bash
#!/bin/bash
for mesh in *.msh; do
    echo "Processing $mesh"
    gmshparser "$mesh" nodes > "${mesh%.msh}_nodes.txt"
    gmshparser "$mesh" elements > "${mesh%.msh}_elements.txt"
done
```

### 5. Data Validation

Quickly check mesh integrity:

```bash
# Check if mesh has nodes
if [ $(gmshparser mesh.msh nodes | head -n 1) -gt 0 ]; then
    echo "Mesh has nodes"
else
    echo "Warning: Empty mesh"
fi

# Count element types
echo "Element type distribution:"
gmshparser mesh.msh elements | tail -n +2 | awk '{print $2}' | sort | uniq -c
```

## Getting Help

Display CLI help:

```bash
gmshparser --help
```

Or check the version:

```bash
gmshparser --version
```

## Output Redirection

Save output to files:

```bash
# Save nodes
gmshparser mesh.msh nodes > mesh_nodes.txt

# Save elements
gmshparser mesh.msh elements > mesh_elements.txt

# Append to existing file
gmshparser mesh.msh nodes >> all_nodes.txt
```

## Error Handling

The CLI provides clear error messages:

```bash
$ gmshparser nonexistent.msh nodes
Error: File 'nonexistent.msh' not found

$ gmshparser mesh.msh invalid_command
Error: Unknown command 'invalid_command'
Valid commands: nodes, elements
```

## Performance

The CLI is optimized for quick extraction:

- Small meshes (< 10K nodes): Instant
- Medium meshes (10K-100K nodes): < 1 second
- Large meshes (> 100K nodes): Few seconds

## Limitations

- No filtering options (use shell tools like `grep`, `awk`)
- Fixed output format (for flexibility, use the Python API)
- No mesh modification (CLI is read-only)

For more complex operations, use the [Python API](basic-usage.md).

## Next Steps

- Learn about [Visualization](visualization.md)
- Explore the [Python API](basic-usage.md)
- Check [Supported Formats](supported-formats.md)
