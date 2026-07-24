from __future__ import annotations

from collections.abc import Iterable, Mapping
from dataclasses import dataclass
from types import MappingProxyType
from typing import Any

try:
    import numpy as np
    from numpy.typing import DTypeLike, NDArray
except ModuleNotFoundError as error:  # pragma: no cover
    raise ModuleNotFoundError(
        "NumPy support is optional; install it with 'pip install gmshparser[numpy]'"
    ) from error

from .api import Mesh
from .element_types import ElementType

__all__ = ["CellBlock", "MeshArrays", "to_numpy"]


@dataclass(frozen=True, slots=True)
class CellBlock:
    """NumPy arrays for all elements of one Gmsh element type.

    ``connectivity`` contains zero-based row indices into
    :attr:`MeshArrays.points`. Original Gmsh element tags and entity keys remain
    available in arrays with matching row order.
    """

    element_type: ElementType
    connectivity: NDArray[Any]
    element_tags: NDArray[Any]
    entity_keys: NDArray[Any]

    def __post_init__(self) -> None:
        if self.connectivity.ndim != 2:
            raise ValueError("Cell connectivity must be a two-dimensional array")
        if self.element_tags.shape != (len(self.connectivity),):
            raise ValueError("Element tags must have one value per connectivity row")
        if self.entity_keys.shape != (len(self.connectivity), 2):
            raise ValueError("Entity keys must have shape (number_of_elements, 2)")

    @property
    def number_of_elements(self) -> int:
        """Number of elements in this block."""
        return len(self.connectivity)

    @property
    def nodes_per_element(self) -> int:
        """Connectivity width for this element type."""
        return self.connectivity.shape[1]


@dataclass(frozen=True, slots=True)
class MeshArrays:
    """Detached NumPy representation of a modern :class:`gmshparser.api.Mesh`.

    Element blocks are keyed by :class:`~gmshparser.ElementType`. Arrays are
    ordinary writable NumPy copies; changing them does not mutate the source
    mesh.
    """

    points: NDArray[Any]
    node_tags: NDArray[Any]
    node_entity_keys: NDArray[Any]
    cells: Mapping[ElementType, CellBlock]

    def __post_init__(self) -> None:
        if self.points.ndim != 2 or self.points.shape[1] != 3:
            raise ValueError("Points must have shape (number_of_nodes, 3)")
        if self.node_tags.shape != (len(self.points),):
            raise ValueError("Node tags must have one value per point")
        if self.node_entity_keys.shape != (len(self.points), 2):
            raise ValueError("Node entity keys must have shape (number_of_nodes, 2)")

    @property
    def element_types(self) -> tuple[ElementType, ...]:
        """Element types in first-appearance order."""
        return tuple(self.cells)

    @property
    def number_of_nodes(self) -> int:
        """Number of point rows."""
        return len(self.points)

    @property
    def number_of_elements(self) -> int:
        """Total number of elements across all cell blocks."""
        return sum(block.number_of_elements for block in self.cells.values())

    def cell_block(self, element_type: ElementType | int) -> CellBlock:
        """Return the block for one numeric or named Gmsh element type."""
        return self.cells[ElementType(element_type)]

    def cell_node_tags(self, element_type: ElementType | int) -> NDArray[Any]:
        """Return original Gmsh node tags with the block connectivity shape."""
        block = self.cell_block(element_type)
        return self.node_tags[block.connectivity]


def to_numpy(
    mesh: Mesh,
    *,
    element_types: Iterable[ElementType | int] | ElementType | int | None = None,
    coordinate_dtype: DTypeLike = np.float64,
    index_dtype: DTypeLike = np.int64,
) -> MeshArrays:
    """Convert a modern mesh into detached NumPy arrays.

    Parameters
    ----------
    mesh
        Mesh returned by :func:`gmshparser.read` or
        :func:`gmshparser.api.parse`.
    element_types
        Optional element type or iterable of types to include. Nodes are kept
        intact so connectivity always indexes the same ``points`` array.
    coordinate_dtype
        NumPy dtype for Cartesian coordinates.
    index_dtype
        Integer NumPy dtype for tags, entity keys, and connectivity indices.

    Returns
    -------
    MeshArrays
        Points, original node tags, node entity keys, and rectangular cell
        blocks grouped by element type.
    """
    if not isinstance(mesh, Mesh):
        raise TypeError(
            "to_numpy() requires the modern mesh returned by gmshparser.read()"
        )

    resolved_index_dtype = np.dtype(index_dtype)
    if not np.issubdtype(resolved_index_dtype, np.integer):
        raise TypeError("index_dtype must be an integer NumPy dtype")

    wanted_types = _normalize_element_types(element_types)
    nodes = tuple(mesh.nodes)

    points = np.asarray(
        [node.coordinates for node in nodes], dtype=coordinate_dtype
    ).reshape((-1, 3))
    node_tags = np.asarray([node.tag for node in nodes], dtype=resolved_index_dtype)
    node_entity_keys = np.asarray(
        [node.entity_key for node in nodes], dtype=resolved_index_dtype
    ).reshape((-1, 2))

    tag_to_row = {node.tag: row for row, node in enumerate(nodes)}
    grouped: dict[ElementType, list] = {}
    for element in mesh.elements:
        if wanted_types is None or element.element_type in wanted_types:
            grouped.setdefault(element.element_type, []).append(element)

    blocks: dict[ElementType, CellBlock] = {}
    for element_type, elements in grouped.items():
        widths = {len(element.nodes) for element in elements}
        if len(widths) != 1:
            raise ValueError(
                f"Element type {element_type.name} has inconsistent connectivity widths"
            )
        width = widths.pop()
        connectivity = np.empty((len(elements), width), dtype=resolved_index_dtype)

        for element_row, element in enumerate(elements):
            for node_column, node in enumerate(element.nodes):
                try:
                    connectivity[element_row, node_column] = tag_to_row[node.tag]
                except KeyError as error:
                    raise ValueError(
                        f"Element {element.tag} references node {node.tag}, "
                        "which is not present in mesh.nodes"
                    ) from error

        blocks[element_type] = CellBlock(
            element_type=element_type,
            connectivity=connectivity,
            element_tags=np.asarray(
                [element.tag for element in elements], dtype=resolved_index_dtype
            ),
            entity_keys=np.asarray(
                [element.entity_key for element in elements],
                dtype=resolved_index_dtype,
            ).reshape((-1, 2)),
        )

    return MeshArrays(
        points=points,
        node_tags=node_tags,
        node_entity_keys=node_entity_keys,
        cells=MappingProxyType(blocks),
    )


def _normalize_element_types(
    element_types: Iterable[ElementType | int] | ElementType | int | None,
) -> frozenset[ElementType] | None:
    if element_types is None:
        return None
    if isinstance(element_types, int):
        return frozenset((ElementType(element_types),))
    return frozenset(ElementType(value) for value in element_types)
