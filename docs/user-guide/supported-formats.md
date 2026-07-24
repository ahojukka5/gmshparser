# Supported Formats

gmshparser reads the node and element data from selected **ASCII** Gmsh MSH
formats. The version is detected automatically from `$MeshFormat`, or from the
legacy `$NOD` header for MSH 1.0.

## Supported versions

| Version | Node and element layout | Status |
| --- | --- | --- |
| MSH 1.0 | legacy `$NOD` and `$ELM` sections | supported |
| MSH 2.0 | flat `$Nodes` and `$Elements` sections | supported |
| MSH 2.1 | flat `$Nodes` and `$Elements` sections | supported |
| MSH 2.2 | flat `$Nodes` and `$Elements` sections | supported |
| MSH 4.0 | entity-block `$Nodes` and `$Elements` sections | supported |
| MSH 4.1 | entity-block `$Nodes` and `$Elements` sections | supported |

“Supported” here means that the core mesh topology—node coordinates, element
connectivity, entity grouping, counts, and tag ranges—can be read through the
common Python API. It does not mean that every optional MSH section is retained.

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

The parser converts the legacy flat data into the same `Mesh`, `NodeEntity`, and
`ElementEntity` model used for later versions.

## MSH 2.x

For MSH 2.0, 2.1, and 2.2, gmshparser parses:

- `$MeshFormat`
- `$Nodes`
- `$Elements`

Element records may contain physical, elementary, and partition tags. The
current parser uses the elementary entity tag for grouping but does not expose
the complete tag list on each element.

`$PhysicalNames` and other optional sections are not stored by the current data
model.

## MSH 4.x

For MSH 4.0 and 4.1, gmshparser parses the entity-block forms of `$Nodes` and
`$Elements` and stores each block as a node or element entity.

The standalone `$Entities` section and its geometry, bounding boxes, topology,
and physical tags are not retained. Entity dimension and tag values available
in the node and element block headers are preserved.

## Common limitations

The current reader does not provide:

- binary MSH support
- mesh writing or format conversion
- compressed-file handling
- preservation of every optional MSH section
- post-processing datasets such as `$NodeData`, `$ElementData`, or
  `$ElementNodeData`
- periodic-entity metadata
- complete physical-name and physical-tag metadata

Unknown sections are skipped by the main parsing loop unless a parser for that
section is registered in the relevant version-specific parser list.

## Element types

Element type codes are stored as the numeric values defined by Gmsh. Common
codes include:

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

```python
import gmshparser

mesh = gmshparser.parse("mesh.msh")
print(mesh.get_version())
print(mesh.is_ascii())
```

## Test coverage

Repository test data includes files for each supported version family. Exact
test and coverage totals are intentionally not duplicated here; the current
GitHub Actions run is authoritative. See [Test Results](../developer-guide/test-results.md).
