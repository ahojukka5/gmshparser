from __future__ import annotations

import os
from collections.abc import Iterable, Iterator
from dataclasses import dataclass
from typing import Generic, TextIO, TypeVar, cast

from .main_parser import MainParser
from .mesh import Mesh as LegacyMesh

T = TypeVar("T")
E = TypeVar("E")


class TaggedCollection(Generic[T]):
    """Immutable values that iterate naturally and can be indexed by tag.

    Iteration yields objects rather than tags:

    >>> for node in mesh.nodes:
    ...     print(node.tag)

    Integer indexing uses the Gmsh tag:

    >>> node = mesh.nodes[42]
    """

    __slots__ = ("_items", "_by_tag")

    def __init__(self, items: Iterable[T]):
        self._items = tuple(items)
        self._by_tag = {item.tag: item for item in self._items}
        if len(self._by_tag) != len(self._items):
            raise ValueError("Tags must be unique within a mesh collection")

    def __iter__(self) -> Iterator[T]:
        return iter(self._items)

    def __len__(self) -> int:
        return len(self._items)

    def __getitem__(self, tag: int) -> T:
        return self._by_tag[tag]

    def __contains__(self, value: object) -> bool:
        if isinstance(value, int):
            return value in self._by_tag
        return value in self._items

    def __repr__(self) -> str:
        return f"{type(self).__name__}({list(self._items)!r})"

    def __eq__(self, other: object) -> bool:
        return type(self) is type(other) and self._items == other._items

    def __hash__(self) -> int:
        return hash(self._items)

    def get(self, tag: int, default: T | None = None) -> T | None:
        """Return the item with *tag*, or *default* when it is absent."""
        return self._by_tag.get(tag, default)

    @property
    def tags(self) -> tuple[int, ...]:
        """Return tags in parser order."""
        return tuple(self._by_tag)


@dataclass(frozen=True, slots=True)
class Node:
    """An immutable mesh node.

    Attributes
    ----------
    tag
        Globally unique Gmsh node tag.
    coordinates
        ``(x, y, z)`` coordinates.
    dimension
        Dimension of the owning Gmsh entity.
    entity_tag
        Tag of the owning Gmsh entity.
    """

    tag: int
    coordinates: tuple[float, float, float]
    dimension: int
    entity_tag: int

    @property
    def x(self) -> float:
        """X coordinate."""
        return self.coordinates[0]

    @property
    def y(self) -> float:
        """Y coordinate."""
        return self.coordinates[1]

    @property
    def z(self) -> float:
        """Z coordinate."""
        return self.coordinates[2]

    def __iter__(self) -> Iterator[float]:
        return iter(self.coordinates)


@dataclass(frozen=True, slots=True)
class Element:
    """An immutable mesh element with its Gmsh entity context."""

    tag: int
    element_type: int
    node_tags: tuple[int, ...]
    dimension: int
    entity_tag: int

    @property
    def type(self) -> int:
        """Numeric Gmsh element type."""
        return self.element_type

    @property
    def connectivity(self) -> tuple[int, ...]:
        """Alias for :attr:`node_tags`."""
        return self.node_tags

    def __iter__(self) -> Iterator[int]:
        return iter(self.node_tags)

    def __len__(self) -> int:
        return len(self.node_tags)


class NodeCollection(TaggedCollection[Node]):
    """All nodes in a mesh or entity."""

    def where(
        self,
        *,
        dimension: int | None = None,
        entity_tag: int | None = None,
    ) -> NodeCollection:
        """Return nodes matching the supplied entity metadata."""
        return NodeCollection(
            node
            for node in self
            if (dimension is None or node.dimension == dimension)
            and (entity_tag is None or node.entity_tag == entity_tag)
        )

    @property
    def coordinates(self) -> tuple[tuple[float, float, float], ...]:
        """Return coordinates in collection order."""
        return tuple(node.coordinates for node in self)


class ElementCollection(TaggedCollection[Element]):
    """All elements in a mesh or entity."""

    def where(
        self,
        *,
        element_type: int | None = None,
        dimension: int | None = None,
        entity_tag: int | None = None,
    ) -> ElementCollection:
        """Return elements matching the supplied metadata."""
        return ElementCollection(
            element
            for element in self
            if (element_type is None or element.element_type == element_type)
            and (dimension is None or element.dimension == dimension)
            and (entity_tag is None or element.entity_tag == entity_tag)
        )

    def by_type(self, element_type: int) -> ElementCollection:
        """Return elements with one numeric Gmsh element type."""
        return self.where(element_type=element_type)

    @property
    def types(self) -> frozenset[int]:
        """Return numeric Gmsh element types present in the collection."""
        return frozenset(element.element_type for element in self)


@dataclass(frozen=True, slots=True)
class NodeEntity:
    """A Gmsh node entity and the nodes assigned to it."""

    dimension: int
    tag: int
    parametric_coordinates: int
    nodes: NodeCollection

    def __iter__(self) -> Iterator[Node]:
        return iter(self.nodes)

    def __len__(self) -> int:
        return len(self.nodes)


@dataclass(frozen=True, slots=True)
class ElementEntity:
    """A Gmsh element entity and the elements assigned to it."""

    dimension: int
    tag: int
    element_type: int
    elements: ElementCollection

    @property
    def type(self) -> int:
        """Numeric Gmsh element type shared by the entity."""
        return self.element_type

    def __iter__(self) -> Iterator[Element]:
        return iter(self.elements)

    def __len__(self) -> int:
        return len(self.elements)


class EntityCollection(Generic[E]):
    """Immutable entities keyed by ``(dimension, tag)``."""

    __slots__ = ("_items", "_by_key")

    def __init__(self, items: Iterable[E]):
        self._items = tuple(items)
        self._by_key = {(item.dimension, item.tag): item for item in self._items}
        if len(self._by_key) != len(self._items):
            raise ValueError("Entity keys must be unique")

    def __iter__(self) -> Iterator[E]:
        return iter(self._items)

    def __len__(self) -> int:
        return len(self._items)

    def __getitem__(self, key: tuple[int, int]) -> E:
        return self._by_key[key]

    def __contains__(self, value: object) -> bool:
        if isinstance(value, tuple) and len(value) == 2:
            return value in self._by_key
        return value in self._items

    def __repr__(self) -> str:
        return f"{type(self).__name__}({list(self._items)!r})"

    def __eq__(self, other: object) -> bool:
        return type(self) is type(other) and self._items == other._items

    def __hash__(self) -> int:
        return hash(self._items)

    def get(self, key: tuple[int, int], default: E | None = None) -> E | None:
        """Return an entity by ``(dimension, tag)``."""
        return self._by_key.get(key, default)

    def where(self, *, dimension: int | None = None) -> EntityCollection[E]:
        """Return entities matching a dimension."""
        return EntityCollection(
            entity
            for entity in self
            if dimension is None or entity.dimension == dimension
        )

    @property
    def keys(self) -> tuple[tuple[int, int], ...]:
        """Return ``(dimension, tag)`` keys in parser order."""
        return tuple(self._by_key)


@dataclass(frozen=True, slots=True)
class Mesh:
    """A read-only, Pythonic representation of a parsed Gmsh mesh."""

    name: str
    version: float | None
    version_info: tuple[int, int] | None
    is_ascii: bool
    precision: int
    nodes: NodeCollection
    elements: ElementCollection
    node_entities: EntityCollection[NodeEntity]
    element_entities: EntityCollection[ElementEntity]

    @classmethod
    def from_legacy(cls, mesh: LegacyMesh) -> Mesh:
        """Build the modern model from the compatibility model."""
        nodes: list[Node] = []
        node_entities: list[NodeEntity] = []

        for legacy_entity in mesh.get_node_entities():
            dimension = legacy_entity.get_dimension()
            entity_tag = legacy_entity.get_tag()
            entity_nodes = [
                Node(
                    tag=legacy_node.get_tag(),
                    coordinates=tuple(legacy_node.get_coordinates()),
                    dimension=dimension,
                    entity_tag=entity_tag,
                )
                for legacy_node in legacy_entity.get_nodes()
            ]
            collection = NodeCollection(entity_nodes)
            nodes.extend(collection)
            node_entities.append(
                NodeEntity(
                    dimension=dimension,
                    tag=entity_tag,
                    parametric_coordinates=(
                        legacy_entity.get_number_of_parametric_coordinates()
                    ),
                    nodes=collection,
                )
            )

        elements: list[Element] = []
        element_entities: list[ElementEntity] = []

        for legacy_entity in mesh.get_element_entities():
            dimension = legacy_entity.get_dimension()
            entity_tag = legacy_entity.get_tag()
            element_type = legacy_entity.get_element_type()
            entity_elements = [
                Element(
                    tag=legacy_element.get_tag(),
                    element_type=element_type,
                    node_tags=tuple(legacy_element.get_connectivity()),
                    dimension=dimension,
                    entity_tag=entity_tag,
                )
                for legacy_element in legacy_entity.get_elements()
            ]
            collection = ElementCollection(entity_elements)
            elements.extend(collection)
            element_entities.append(
                ElementEntity(
                    dimension=dimension,
                    tag=entity_tag,
                    element_type=element_type,
                    elements=collection,
                )
            )

        major = mesh.get_version_major()
        minor = mesh.get_version_minor()
        version_info = None if major is None or minor is None else (major, minor)

        return cls(
            name=mesh.get_name(),
            version=mesh.get_version(),
            version_info=version_info,
            is_ascii=mesh.get_ascii(),
            precision=mesh.get_precision(),
            nodes=NodeCollection(nodes),
            elements=ElementCollection(elements),
            node_entities=EntityCollection(node_entities),
            element_entities=EntityCollection(element_entities),
        )

    @property
    def bounds(
        self,
    ) -> tuple[tuple[float, float, float], tuple[float, float, float]] | None:
        """Return axis-aligned ``(minimum, maximum)`` coordinates."""
        if not self.nodes:
            return None

        coordinates = self.nodes.coordinates
        minimum = tuple(min(axis) for axis in zip(*coordinates, strict=True))
        maximum = tuple(max(axis) for axis in zip(*coordinates, strict=True))
        return minimum, maximum

    def __repr__(self) -> str:
        return (
            f"Mesh(name={self.name!r}, version={self.version!r}, "
            f"nodes={len(self.nodes)}, elements={len(self.elements)})"
        )

    __str__ = __repr__


def read(
    source: str | os.PathLike[str] | TextIO,
    *,
    name: str | None = None,
) -> Mesh:
    """Read a path or text stream into the modern API.

    Parameters
    ----------
    source
        Filesystem path or an open text stream.
    name
        Optional source name for streams. Paths use their own string value.

    Returns
    -------
    Mesh
        Immutable mesh with flat, tag-addressable collections.

    Notes
    -----
    Use :func:`gmshparser.parse` when the compatibility API is required.
    """
    if hasattr(source, "read"):
        stream = cast(TextIO, source)
        mesh_name = name or str(getattr(stream, "name", "<stream>"))
        return _read_stream(stream, mesh_name)

    path = os.fspath(source)
    with open(path, encoding="utf-8") as stream:
        return _read_stream(stream, name or path)


def _read_stream(stream: TextIO, name: str) -> Mesh:
    legacy_mesh = LegacyMesh()
    legacy_mesh.set_name(name)
    MainParser().parse(legacy_mesh, stream)
    return Mesh.from_legacy(legacy_mesh)
