# Physical Groups and Periodicity

Physical groups give application meaning to geometric entities and elements. Periodic links describe slave-to-master entity and node relationships. Both are available from the modern model returned by `gmshparser.read()`.

## Physical groups

Named groups from `$PhysicalNames` and assignments from supported MSH sections are collected in `mesh.physical_groups`.

```python
import gmshparser

mesh = gmshparser.read("mesh.msh")

walls = mesh.physical_groups["Walls"]
domain = mesh.physical_groups[(3, 2)]
```

A name lookup is valid only when the name is unique. Use `(dimension, tag)` when the same name appears in more than one dimension.

```python
print(walls.dimension)
print(walls.tag)
print(walls.name)
print(walls.entities)
print(walls.elements)
print(walls.nodes)
```

The convenience method accepts a name or numeric tag:

```python
walls = mesh.physical_group("Walls")
domain = mesh.physical_group(2, dimension=3)
```

A numeric tag without `dimension=` is accepted only when it identifies one group unambiguously.

## Filter by physical tag

Physical assignments are also available directly on nodes, elements, and entities.

```python
wall_elements = mesh.elements.where(physical_tag=10)
wall_nodes = mesh.nodes.where(physical_tag=10)
wall_entities = mesh.entities.where(physical_tag=10)
```

Use `mesh.physical_groups` when you need the resolved group object and its name. Use collection filters when the tag is already known and you only need selected mesh values.

## Anonymous groups

MSH 1.0 and files without `$PhysicalNames` may contain physical assignments without names. These groups remain accessible by `(dimension, tag)`:

```python
boundary = mesh.physical_groups[(2, 10)]
assert boundary.name is None
```

## Periodic links

Supported MSH 2.x and 4.x `$Periodic` sections are exposed through `mesh.periodic_links`.

```python
link = mesh.periodic_links[(2, 7)]

print(link.dimension)
print(link.entity_tag)
print(link.master_entity_tag)
print(link.affine_transform)
print(link.node_pairs)
```

Each node pair is `(slave_node_tag, master_node_tag)` in file order:

```python
for slave_tag, master_tag in link.node_pairs:
    slave = mesh.nodes[slave_tag]
    master = mesh.nodes[master_tag]
    print(slave.coordinates, master.coordinates)
```

Filter periodic relations by dimension:

```python
surface_links = mesh.periodic_links.by_dimension(2)
```

The convenience method avoids constructing a tuple key:

```python
link = mesh.periodic_link(dimension=2, tag=7)
```

## Compatibility API

The original mutable model exposes periodic data through `get_periodic_link()` and `get_periodic_links()`. Physical names and assignments are also retained, but new code should prefer the resolved modern collections.

See [Modern Data Model](pythonic-api.md) for collection behavior and [Supported Formats](supported-formats.md) for version-specific retention rules.
