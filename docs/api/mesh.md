# Mesh API

::: gmshparser.mesh.Mesh
    options:
      show_source: true
      heading_level: 2

## Usage Examples

### Basic Information

```python
mesh = gmshparser.parse("mesh.msh")

# Version info
version = mesh.get_version()
is_ascii = mesh.is_ascii()

# Counts
num_nodes = mesh.get_number_of_nodes()
num_elements = mesh.get_number_of_elements()
num_node_entities = mesh.get_number_of_node_entities()
num_element_entities = mesh.get_number_of_element_entities()

# Tag ranges
min_node_tag = mesh.get_min_node_tag()
max_node_tag = mesh.get_max_node_tag()
min_element_tag = mesh.get_min_element_tag()
max_element_tag = mesh.get_max_element_tag()
```

### Accessing Data

```python
# Get all node entities
node_entities = mesh.get_node_entities()

# Get all element entities
element_entities = mesh.get_element_entities()

# Get mesh name (filename)
name = mesh.get_name()
```

## Related Classes

- [Node](../api/overview.md#node) - Individual node
- [NodeEntity](../api/overview.md#nodeentity) - Group of nodes
- [Element](../api/overview.md#element) - Individual element
- [ElementEntity](../api/overview.md#elemententity) - Group of elements
