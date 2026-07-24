# Supported Formats

gmshparser reads mesh topology and physical group metadata from selected
**ASCII** Gmsh MSH formats. The version is detected automatically from
`$MeshFormat`, or from the legacy `$NOD` header for MSH 1.0.

## Supported versions

| Version | Node and element layout | Physical groups | Status |
| --- | --- | --- | --- |
| MSH 1.0 | legacy `$NOD` and `$ELM` sections | element region fields | supported |
| MSH 2.0 | flat `$Nodes` and `$Elements` sections | element tags and `$PhysicalNames` | supported |
| MSH 2.1 | flat `$Nodes` and `$Elements` sections | element tags and `$PhysicalNames` | supported |
| MSH 2.2 | flat `$Nodes` and `$Elements` sections | element tags and `$PhysicalNames` | supported |
| MSH 4.0 | entity-block `$Nodes` and `$Elements` sections | `$Entities` and `$PhysicalNames` | supported |
| MSH 4.1 | entity-block `$Nodes` and `$Elements` sections | `$Entities` and `$PhysicalNames` | supported |

“Supported” means that core topology—node coordinates, element connectivity,
entity grouping, counts, tag ranges, and physical group assignments—can be read.
It does not mean that every optional MSH section or every geometry relationship
is retained.

## ASCII only

The `$MeshFormat` file-type field is recorded in the `Mesh` object, but the
parser reads the file as text. Binary MSH files are therefore not supported.
Export them from Gmsh with `Mesh.Binary = 0` and select a supported MSH version
before parsing.

## MSH 1.0

MSH 1.0 files have no `$MeshFormat` section. gmshparser recognizes the legacy
headers:

```text
$NOD
<number-of-nodes>
<node-id> <x> <y> <z>
...
$ENDNOD
$ELM
<number-of-elements>
<element-records>
...
$ENDELM
```

The `reg-phys` and `reg-elem` fields in element records are retained as physical
and elementary entity assignments. MSH 1.0 does not carry the later named
`$PhysicalNames` section, so these groups may be anonymous.

## MSH 2.x

For MSH 2.0, 2.1, and 2.2, gmshparser parses:

- `$MeshFormat`
- `$PhysicalNames`, when present
- `$Nodes`
- `$Elements`

The first element tag is retained as the physical group tag and the second as
the elementary entity tag. Additional optional element tags, such as partition
metadata, are not yet exposed individually.

## MSH 4.x

For MSH 4.0 and 4.1, gmshparser parses:

- `$MeshFormat`
- `$PhysicalNames`, when present
- physical tag assignments from `$Entities`
- entity-block `$Nodes`
- entity-block `$Elements`

The physical assignments are retained, but other `$Entities` information such as
bounding boxes, boundary topology, and geometry parametrization is not yet part
of the public model.

## Physical group access

The modern API resolves physical groups into their entities, elements, and
participating nodes:

```python
import gmshparser

mesh = gmshparser.read("mesh.msh")
walls = mesh.physical_groups["Walls"]

print(walls.entities)
print(walls.elements)
print(walls.nodes)
```

Anonymous groups remain available by `(dimension, tag)`.

## Common limitations

The current reader does not provide:

- binary MSH support
- mesh writing or format conversion
- compressed-file handling
- preservation of every optional MSH section
- post-processing datasets such as `$NodeData`, `$ElementData`, or
  `$ElementNodeData`
- periodic-entity metadata
- MSH 4 entity bounding boxes and boundary topology
- the complete list of auxiliary MSH 2.x element tags

Unknown sections are skipped by the main parsing loop unless a parser for that
section is registered in the relevant version-specific parser list.

## Element types

The modern API represents element type codes as `ElementType` integer-enum
values. Common codes include:

| Code | Element | Dimension |
| --- | --- | --- |
| 15 | point | 0 |
| 1 | two-node line | 1 |
| 2 | three-node triangle | 2 |
| 3 | four-node quadrangle | 2 |
| 4 | four-node tetrahedron | 3 |
| 5 | eight-node hexahedron | 3 |
| 6 | six-node prism | 3 |
| 7 | five-node pyramid | 3 |

The parser also recognizes several higher-order element codes when deriving the
entity dimension. Refer to the official Gmsh MSH specification for the complete
code table.

## Check the detected format

Modern API:

```python
mesh = gmshparser.read("mesh.msh")
print(mesh.version)
print(mesh.is_ascii)
```

Compatibility API:

```python
mesh = gmshparser.parse("mesh.msh")
print(mesh.get_version())
print(mesh.get_ascii())
```

## Test coverage

Repository test data includes files for each supported version family. Exact
test and coverage totals are intentionally not duplicated here; the current
GitHub Actions run is authoritative. See [Test Results](../developer-guide/test-results.md).
