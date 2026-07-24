from __future__ import annotations

import os
from collections.abc import Iterable, Iterator
from dataclasses import dataclass
from enum import IntEnum
from typing import TextIO, cast

from .main_parser import MainParser
from .mesh import Mesh as LegacyMesh

__all__ = [
    "Element",
    "ElementCollection",
    "ElementType",
    "Entity",
    "EntityCollection",
    "EntityKey",
    "Mesh",
    "Node",
    "NodeCollection",
    "Version",
    "read",
]


type EntityKey = tuple[int, int]


@dataclass(frozen=True, order=True, slots=True)
class Version:
    """A semantic MSH format version such as ``4.1``."""

    major: int
    minor: int

    def __str__(self) -> str:
        return f"{self.major}.{self.minor}"

    def __float__(self) -> float:
        return float(str(self))


class ElementType(IntEnum):
    """Common numeric element types from the Gmsh MSH specification.

    Values not named here are still accepted and represented as ``TYPE_<id>``
    pseudo-members, so higher-order and future element types remain usable.
    """

    LINE = 1
    TRIANGLE = 2
    QUADRANGLE = 3
    TETRAHEDRON = 4
    HEXAHEDRON = 5
    PRISM = 6
    PYRAMID = 7
    SECOND_ORDER_LINE = 8
    SECOND_ORDER_TRIANGLE = 9
    SECOND_ORDER_QUADRANGLE = 10
    SECOND_ORDER_TETRAHEDRON = 11
    SECOND_ORDER_HEXAHEDRON = 12
    SECOND_ORDER_PRISM = 13
    SECOND_ORDER_PYRAMID = 14
    POINT = 15

    @classmethod
    def _missing_(cls, value: object) -> ElementType | None:
        if not isinstance(value, int):
            return None

        member = int.__new__(cls, value)
        member._name_ = f"TYPE_{value}"
        member._value_ = value
        cls._value2member_map_[value] = member
        return member


class _TaggedCollection[T]:
    """Immutable values that iterate naturally and index by Gmsh tag."""

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
        """Return the item with *tag*, or *default* when absent."""
        return self._by_tag.get(tag, default)

    @property
    def tags(self) -> tuple[int, ...]:
        """Return tags in parser order."""
        return tuple(self._by_tag)


@dataclass(frozen=True, slots=True)
class Node:
    """An immutable mesh node.

    ``coordinates`` always contains the Cartesian ``(x, y, z)`` values.
    Additional coordinates from parametric MSH node blocks are available in
    ``parametric_coordinates``.
    """

    tag: int
    coordinates: tuple[float, float, float]
    dimension: int
    entity_tag: int
    parametric_coordinates: tuple[float, ...] = ()

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

    @property
    def entity_key(self) -> EntityKey:
        """Owning entity as ``(dimension, tag)``."""
        return self.dimension, self.entity_tag

    @property
    def is_parametric(self) -> bool:
        """Whether the node carries parametric coordinates."""
        return bool(self.parametric_coordinates)

    def __iter__(self) -> Iterator[float]:
        return iter(self.coordinates)


@dataclass(frozen=True, slots=True)
class Element:
    """An immutable element with direct references to its nodes."""

    tag: int
    type: ElementType
    nodes: tuple[Node, ...]
    dimension: int
    entity_tag: int

    @property
    def element_type(self) -> ElementType:
        """Descriptive alias for :attr:`type`."""
        return self.type

    @property
    def type_id(self) -> int:
        """Raw numeric Gmsh element type."""
        return int(self.type)

    @property
    def node_tags(self) -> tuple[int, ...]:
        """Connectivity as original Gmsh node tags."""
        return tuple(node.tag for node in self.nodes)

    @property
    def connectivity(self) -> tuple[int, ...]:
        """Alias for :attr:`node_tags`."""
        return self.node_tags

    @property
    def entity_key(self) -> EntityKey:
        """Owning entity as ``(dimension, tag)``."""
        return self.dimension, self.entity_tag

    def __iter__(self) -> Iterator[Node]:
        return iter(self.nodes)

    def __len__(self) -> int:
        return len(self.nodes)


class NodeCollection(_TaggedCollection[Node]):
    """All nodes in a mesh, entity, or filtered selection."""

    def where(
        self,
        *,
        dimension: int | None = None,
        entity_tag: int | None = None,
        entity: EntityKey | None = None,
        parametric: bool | None = None,
    ) -> NodeCollection:
        """Return nodes matching the supplied metadata."""
        if entity is not None:
            dimension, entity_tag = entity

        return NodeCollection(
            node
            for node in self
            if (dimension is None or node.dimension == dimension)
            and (entity_tag is None or node.entity_tag == entity_tag)
            and (parametric is None or node.is_parametric is parametric)
        )

    @property
    def coordinates(self) -> tuple[tuple[float, float, float], ...]:
        """Cartesian coordinates in collection order."""
        return tuple(node.coordinates for node in self)


class ElementCollection(_TaggedCollection[Element]):
    """All elements in a mesh, entity, or filtered selection."""

    def where(
        self,
        *,
        element_type: ElementType | int | None = None,
        dimension: int | None = None,
        entity_tag: int | None = None,
        entity: EntityKey | None = None,
    ) -> ElementCollection:
        """Return elements matching the supplied metadata."""
        if entity is not None:
            dimension, entity_tag = entity
        wanted_type = None if element_type is None else ElementType(element_type)

        return ElementCollection(
            element
            for element in self
            if (wanted_type is None or element.type is wanted_type)
            and (dimension is None or element.dimension == dimension)
            and (entity_tag is None or element.entity_tag == entity_tag)
        )

    def by_type(self, element_type: ElementType | int) -> ElementCollection:
        """Return elements with one Gmsh element type."""
        return self.where(element_type=element_type)

    @property
    def types(self) -> frozenset[ElementType]:
        """Element types present in the collection."""
        return frozenset(element.type for element in self)


@dataclass(frozen=True, slots=True)
class Entity:
    """A unified Gmsh entity containing both nodes and elements."""

    dimension: int
    tag: int
    nodes: NodeCollection
    elements: ElementCollection

    @property
    def key(self) -> EntityKey:
        """Entity key as ``(dimension, tag)``."""
        return self.dimension, self.tag

    @property
    def element_types(self) -> frozenset[ElementType]:
        """Element types assigned to this entity."""
        return self.elements.types

    @property
    def has_parametric_nodes(self) -> bool:
        """Whether any node carries parametric coordinates."""
        return any(node.is_parametric for node in self.nodes)


class EntityCollection:
    """Immutable entities keyed by ``(dimension, tag)``."""

    __slots__ = ("_items", "_by_key")

    def __init__(self, items: Iterable[Entity]):
        self._items = tuple(items)
        self._by_key = {entity.key: entity for entity in self._items}
        if len(self._by_key) != len(self._items):
            raise ValueError("Entity keys must be unique")

    def __iter__(self) -> Iterator[Entity]:
        return iter(self._items)

    def __len__(self) -> int:
        return len(self._items)

    def __getitem__(self, key: EntityKey) -> Entity:
        return self._by_key[key]

    def __contains__(self, value: object) -> bool:
        if isinstance(value, tuple) and len(value) == 2:
            return value in self._by_key
        return value in self._items

    def __repr__(self) -> str:
        return f"EntityCollection({list(self._items)!r})"

    def __eq__(self, other: object) -> bool:
        return isinstance(other, EntityCollection) and self._items == other._items

    def __hash__(self) -> int:
        return hash(self._items)

    def get(
        self,
        key: EntityKey,
        default: Entity | None = None,
    ) -> Entity | None:
        """Return an entity by ``(dimension, tag)``."""
        return self._by_key.get(key, default)

    def where(
        self,
        *,
        dimension: int | None = None,
        element_type: ElementType | int | None = None,
        has_nodes: bool | None = None,
        has_elements: bool | None = None,
    ) -> EntityCollection:
        """Return entities matching dimension, contents, or element type."""
        wanted_type = None if element_type is None else ElementType(element_type)
        return EntityCollection(
            entity
            for entity in self
            if (dimension is None or entity.dimension == dimension)
            and (has_nodes is None or bool(entity.nodes) is has_nodes)
            and (has_elements is None or bool(entity.elements) is has_elements)
            and (wanted_type is None or wanted_type in entity.element_types)
        )

    @property
    def keys(self) -> tuple[EntityKey, ...]:
        """Entity keys in parser order."""
        return tuple(self._by_key)


@dataclass(frozen=True, slots=True)
class Mesh:
    """A read-only, Pythonic representation of a parsed Gmsh mesh."""

    name: str
    version: Version | None
    is_ascii: bool
    data_size: int
    nodes: NodeCollection
    elements: ElementCollection
    entities: EntityCollection

    @classmethod
    def from_legacy(cls, mesh: LegacyMesh) -> Mesh:
        """Build the modern model from the compatibility model."""
        nodes_by_entity: dict[EntityKey, list[Node]] = {}
        all_nodes: list[Node] = []

        for legacy_entity in mesh.get_node_entities():
            key = legacy_entity.get_dimension(), legacy_entity.get_tag()
            entity_nodes = nodes_by_entity.setdefault(key, [])

            for legacy_node in legacy_entity.get_nodes():
                raw_coordinates = tuple(legacy_node.get_coordinates())
                if len(raw_coordinates) < 3:
                    raise ValueError(
                        f"Node {legacy_node.get_tag()} has fewer than three coordinates"
                    )

                node = Node(
                    tag=legacy_node.get_tag(),
                    coordinates=cast(
                        tuple[float, float, float],
                        raw_coordinates[:3],
                    ),
                    dimension=key[0],
                    entity_tag=key[1],
                    parametric_coordinates=raw_coordinates[3:],
                )
                entity_nodes.append(node)
                all_nodes.append(node)

        nodes = NodeCollection(all_nodes)
        elements_by_entity: dict[EntityKey, list[Element]] = {}
        all_elements: list[Element] = []

        for legacy_entity in mesh.get_element_entities():
            key = legacy_entity.get_dimension(), legacy_entity.get_tag()
            entity_elements = elements_by_entity.setdefault(key, [])
            element_type = ElementType(legacy_entity.get_element_type())

            for legacy_element in legacy_entity.get_elements():
                element_nodes: list[Node] = []
                for node_tag in legacy_element.get_connectivity():
                    node = nodes.get(node_tag)
                    if node is None:
                        raise ValueError(
                            f"Element {legacy_element.get_tag()} references "
                            f"unknown node {node_tag}"
                        )
                    element_nodes.append(node)

                element = Element(
                    tag=legacy_element.get_tag(),
                    type=element_type,
                    nodes=tuple(element_nodes),
                    dimension=key[0],
                    entity_tag=key[1],
                )
                entity_elements.append(element)
                all_elements.append(element)

        elements = ElementCollection(all_elements)
        entity_keys = dict.fromkeys([*nodes_by_entity, *elements_by_entity])
        entities = EntityCollection(
            Entity(
                dimension=dimension,
                tag=tag,
                nodes=NodeCollection(nodes_by_entity.get((dimension, tag), ())),
                elements=ElementCollection(
                    elements_by_entity.get((dimension, tag), ())
                ),
            )
            for dimension, tag in entity_keys
        )

        major = mesh.get_version_major()
        minor = mesh.get_version_minor()
        version = None if major is None or minor is None else Version(major, minor)

        return cls(
            name=mesh.get_name(),
            version=version,
            is_ascii=mesh.get_ascii(),
            data_size=mesh.get_precision(),
            nodes=nodes,
            elements=elements,
            entities=entities,
        )

    @property
    def dimension(self) -> int | None:
        """Highest entity dimension present in the mesh."""
        dimensions = [entity.dimension for entity in self.entities]
        return max(dimensions, default=None)

    @property
    def element_types(self) -> frozenset[ElementType]:
        """Element types present in the mesh."""
        return self.elements.types

    @property
    def bounds(
        self,
    ) -> tuple[tuple[float, float, float], tuple[float, float, float]] | None:
        """Axis-aligned ``(minimum, maximum)`` Cartesian coordinates."""
        if not self.nodes:
            return None

        coordinates = self.nodes.coordinates
        minimum = tuple(min(axis) for axis in zip(*coordinates, strict=True))
        maximum = tuple(max(axis) for axis in zip(*coordinates, strict=True))
        return cast(
            tuple[tuple[float, float, float], tuple[float, float, float]],
            (minimum, maximum),
        )

    def __repr__(self) -> str:
        version = None if self.version is None else str(self.version)
        return (
            f"Mesh(name={self.name!r}, version={version!r}, "
            f"nodes={len(self.nodes)}, elements={len(self.elements)})"
        )

    __str__ = __repr__


def read(
    source: str | os.PathLike[str] | TextIO,
    *,
    name: str | None = None,
) -> Mesh:
    """Read a path or text stream into the modern API.

    Use :func:`gmshparser.parse` when the mutable compatibility API is required.
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
