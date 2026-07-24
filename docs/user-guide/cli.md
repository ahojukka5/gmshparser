# Command-line Interface

The installed `gmshparser` command provides three read-only views of an ASCII
MSH file:

```bash
gmshparser <mesh-file> {info,nodes,elements}
```

Use `uv run gmshparser` when running inside a uv-managed project.

## Mesh summary

```bash
gmshparser mesh.msh info
```

The `info` action prints the same summary as `print(mesh)` in the Python API.

## Nodes

```bash
gmshparser mesh.msh nodes
```

The first line is the total node count. Each following line contains:

```text
node_id x y z
```

Example:

```text
6
1 0.000000 0.000000 0.000000
2 1.000000 0.000000 0.000000
```

## Elements

```bash
gmshparser mesh.msh elements
```

The first line is the total element count. Each following line contains:

```text
element_id element_type node_id...
```

Example:

```text
2
1 3 1 2 3 4
2 3 2 5 6 3
```

## Help and version

```bash
gmshparser --help
gmshparser --version
```

Argument errors are reported by Python's `argparse` command-line parser. File
and parsing errors are currently propagated from the Python API.

## Shell pipelines

Save the output:

```bash
gmshparser mesh.msh nodes > nodes.txt
gmshparser mesh.msh elements > elements.txt
```

Skip the count line and print only node coordinates:

```bash
gmshparser mesh.msh nodes | tail -n +2 | awk '{print $2, $3, $4}'
```

Count element types:

```bash
gmshparser mesh.msh elements \
  | tail -n +2 \
  | awk '{print $2}' \
  | sort \
  | uniq -c
```

## Limitations

- the CLI reads but does not modify meshes
- output formats are fixed and line-oriented
- filtering is delegated to shell tools or the Python API
- only ASCII MSH files supported by the library can be read
