from collections.abc import Iterator
from typing import Any, TextIO

from .parsing import read_required_line


def parse_ints(io: TextIO) -> list[int]:
    """Parse one required line from *io* as integers."""
    line = read_required_line(io, "an integer record")
    return [int(value) for value in line.strip().split()]


def parse_floats(io: TextIO) -> list[float]:
    """Parse one required line from *io* as floating-point values."""
    line = read_required_line(io, "a floating-point record")
    return [float(value) for value in line.strip().split()]


def get_triangles(mesh: Any) -> tuple[list[float], list[float], list[list[int]]]:
    """Return ``(X, Y, triangles)`` for three-node surface triangles.

    Both :func:`gmshparser.read` meshes and compatibility
    :func:`gmshparser.parse` meshes are accepted. Connectivity is converted to
    zero-based indices into ``X`` and ``Y``.
    """
    return _indexed_cells(mesh, element_type=2)


def get_quads(mesh: Any) -> tuple[list[float], list[float], list[list[int]]]:
    """Return ``(X, Y, quads)`` for four-node surface quadrilaterals.

    Both modern and compatibility mesh objects are accepted. Connectivity is
    converted to zero-based indices into ``X`` and ``Y``.
    """
    return _indexed_cells(mesh, element_type=3)


def get_elements_2d(mesh: Any) -> dict[str, Any]:
    """Return node coordinates, triangles, and quadrilaterals for plotting.

    Connectivity in ``triangles`` and ``quads`` retains the original Gmsh node
    tags. The function accepts both the modern and compatibility APIs.
    """
    triangles: list[list[int]] = []
    quads: list[list[int]] = []
    node_ids: set[int] = set()

    for dimension, element_type, _, connectivity in _elements(mesh):
        if dimension != 2:
            continue

        node_ids.update(connectivity)
        if element_type == 2:
            triangles.append(connectivity)
        elif element_type == 3:
            quads.append(connectivity)

    coordinates = dict(_nodes(mesh))
    nodes = {
        tag: (coordinates[tag][0], coordinates[tag][1]) for tag in sorted(node_ids)
    }

    return {
        "nodes": nodes,
        "triangles": triangles,
        "quads": quads,
        "node_ids": sorted(node_ids),
    }


def _indexed_cells(
    mesh: Any,
    *,
    element_type: int,
) -> tuple[list[float], list[float], list[list[int]]]:
    cells: list[list[int]] = []
    node_ids: set[int] = set()

    for dimension, current_type, _, connectivity in _elements(mesh):
        if dimension == 2 and current_type == element_type:
            cells.append(connectivity)
            node_ids.update(connectivity)

    coordinates = dict(_nodes(mesh))
    ordered_tags = sorted(node_ids)
    positions = {tag: index for index, tag in enumerate(ordered_tags)}
    x_coordinates = [coordinates[tag][0] for tag in ordered_tags]
    y_coordinates = [coordinates[tag][1] for tag in ordered_tags]
    indexed_cells = [[positions[tag] for tag in connectivity] for connectivity in cells]
    return x_coordinates, y_coordinates, indexed_cells


def _nodes(
    mesh: Any,
) -> Iterator[tuple[int, tuple[float, float, float]]]:
    if hasattr(mesh, "nodes"):
        for node in mesh.nodes:
            yield node.tag, node.coordinates
        return

    for entity in mesh.get_node_entities():
        for node in entity.get_nodes():
            yield node.get_tag(), tuple(node.get_coordinates())


def _elements(
    mesh: Any,
) -> Iterator[tuple[int, int, int, list[int]]]:
    if hasattr(mesh, "elements"):
        for element in mesh.elements:
            yield (
                element.dimension,
                element.element_type,
                element.tag,
                list(element.node_tags),
            )
        return

    for entity in mesh.get_element_entities():
        dimension = entity.get_dimension()
        element_type = entity.get_element_type()
        for element in entity.get_elements():
            yield (
                dimension,
                element_type,
                element.get_tag(),
                list(element.get_connectivity()),
            )
