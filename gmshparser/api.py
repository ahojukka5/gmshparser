from __future__ import annotations

import os
from collections.abc import Iterable, Iterator
from dataclasses import dataclass, field
from typing import TextIO, cast

from .element_types import ElementFamily, ElementType, ElementTypeInfo
from .main_parser import MainParser
from .mesh import Mesh as LegacyMesh

__all__ = [
    "Element",
    "ElementCollection",
    "ElementFamily",
    "ElementType",
    "ElementTypeInfo",
    "Entity",
    "EntityCollection",
    "EntityKey",
    "Mesh",
    "Node",
    "NodeCollection",
    "PeriodicLink",
    "PeriodicLinkCollection",
    "PeriodicLinkKey",
    "PhysicalGroup",
    "PhysicalGroupCollection",
    "PhysicalGroupKey",
    "Version",
    "parse",
    "read",
]


type EntityKey = tuple[int, int]
type PhysicalGroupKey = tuple[int, int]
type PeriodicLinkKey = tuple[int, int]


@dataclass(frozen=True, order=True, slots=True)
class Version:
    """A semantic MSH format version such as ``4.1``."""

    major: int
    minor: int

    def __str__(self) -> str:
        return f"{self.major}.{self.minor}"

    def __float__(self) -> float:
        return float(str(self))


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
    physical_tags: tuple[int, ...] = ()

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
    element_type: ElementType
    nodes: tuple[Node, ...]
    dimension: int
    entity_tag: int
    physical_tags: tuple[int, ...] = ()

    @property
    def type(self) -> ElementType:
        """Compatibility alias for :attr:`element_type`."""
        return self.element_type

    @property
    def type_id(self) -> int:
        """Raw numeric Gmsh element type."""
        return int(self.element_type)

    @property
    def info(self) -> ElementTypeInfo | None:
        """Registered topology metadata for this element type."""
        return self.element_type.info

    @property
    def family(self) -> ElementFamily | None:
        """Topological element family, or ``None`` when the type is unknown."""
        return self.element_type.family

    @property
    def order(self) -> int | None:
        """Polynomial order, or ``None`` when the type is unknown."""
        return self.element_type.order

    @property
    def expected_node_count(self) -> int | None:
        """Registered connectivity size, or ``None`` when the type is unknown."""
        return self.element_type.node_count

    @property
    def primary_node_count(self) -> int | None:
        """Number of first-order corner nodes, or ``None`` when unknown."""
        return self.element_type.primary_node_count

    @property
    def is_linear(self) -> bool:
        """Whether this is a registered first-order element."""
        return self.element_type.is_linear

    @property
    def is_high_order(self) -> bool:
        """Whether this is a registered second- or higher-order element."""
        return self.element_type.is_high_order

    @property
    def is_complete(self) -> bool | None:
        """Whether all interior high-order nodes are present, or ``None``."""
        return self.element_type.is_complete

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
    """All nodes in a mesh, entity, physical group, or filtered selection."""

    def where(
        self,
        *,
        dimension: int | None = None,
        entity_tag: int | None = None,
        entity: EntityKey | None = None,
        parametric: bool | None = None,
        physical_tag: int | None = None,
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
            and (physical_tag is None or physical_tag in node.physical_tags)
        )

    def by_entity(self, dimension: int, tag: int) -> NodeCollection:
        """Return nodes owned by one elementary entity."""
        return self.where(entity=(dimension, tag))

    @property
    def coordinates(self) -> tuple[tuple[float, float, float], ...]:
        """Cartesian coordinates in collection order."""
        return tuple(node.coordinates for node in self)


class ElementCollection(_TaggedCollection[Element]):
    """All elements in a mesh, entity, physical group, or filtered selection."""

    def where(
        self,
        *,
        element_type: ElementType | int | None = None,
        dimension: int | None = None,
        entity_tag: int | None = None,
        entity: EntityKey | None = None,
        physical_tag: int | None = None,
    ) -> ElementCollection:
        """Return elements matching the supplied metadata."""
        if entity is not None:
            dimension, entity_tag = entity
        wanted_type = None if element_type is None else ElementType(element_type)

        return ElementCollection(
            element
            for element in self
            if (wanted_type is None or element.element_type is wanted_type)
            and (dimension is None or element.dimension == dimension)
            and (entity_tag is None or element.entity_tag == entity_tag)
            and (physical_tag is None or physical_tag in element.physical_tags)
        )

    def by_type(self, element_type: ElementType | int) -> ElementCollection:
        """Return elements with one Gmsh element type."""
        return self.where(element_type=element_type)

    def by_entity(self, dimension: int, tag: int) -> ElementCollection:
        """Return elements owned by one elementary entity."""
        return self.where(entity=(dimension, tag))

    @property
    def types(self) -> frozenset[ElementType]:
        """Element types present in the collection."""
        return frozenset(element.element_type for element in self)


@dataclass(frozen=True, slots=True)
class Entity:
    """A unified Gmsh entity containing both nodes and elements."""

    dimension: int
    tag: int
    nodes: NodeCollection
    elements: ElementCollection
    physical_tags: tuple[int, ...] = ()

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
        physical_tag: int | None = None,
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
            and (physical_tag is None or physical_tag in entity.physical_tags)
        )

    def by_dimension(self, dimension: int) -> EntityCollection:
        """Return entities of one topological dimension."""
        return self.where(dimension=dimension)

    @property
    def keys(self) -> tuple[EntityKey, ...]:
        """Entity keys in parser order."""
        return tuple(self._by_key)


@dataclass(frozen=True, slots=True)
class PeriodicLink:
    """A periodic slave entity and its master-node correspondence."""

    dimension: int
    entity_tag: int
    master_entity_tag: int
    affine_transform: tuple[float, ...] = ()
    node_pairs: tuple[tuple[int, int], ...] = ()

    @property
    def key(self) -> PeriodicLinkKey:
        """Slave entity key as ``(dimension, tag)``."""
        return self.dimension, self.entity_tag

    @property
    def slave_node_tags(self) -> tuple[int, ...]:
        """Slave node tags in file order."""
        return tuple(slave for slave, _ in self.node_pairs)

    @property
    def master_node_tags(self) -> tuple[int, ...]:
        """Master node tags in file order."""
        return tuple(master for _, master in self.node_pairs)


class PeriodicLinkCollection:
    """Immutable periodic links keyed by their slave ``(dimension, tag)``."""

    __slots__ = ("_items", "_by_key")

    def __init__(self, items: Iterable[PeriodicLink]):
        self._items = tuple(items)
        self._by_key = {link.key: link for link in self._items}
        if len(self._by_key) != len(self._items):
            raise ValueError("Periodic link keys must be unique")

    def __iter__(self) -> Iterator[PeriodicLink]:
        return iter(self._items)

    def __len__(self) -> int:
        return len(self._items)

    def __getitem__(self, key: PeriodicLinkKey) -> PeriodicLink:
        return self._by_key[key]

    def __contains__(self, value: object) -> bool:
        if isinstance(value, tuple) and len(value) == 2:
            return value in self._by_key
        return value in self._items

    def __repr__(self) -> str:
        return f"PeriodicLinkCollection({list(self._items)!r})"

    def __eq__(self, other: object) -> bool:
        return isinstance(other, PeriodicLinkCollection) and self._items == other._items

    def __hash__(self) -> int:
        return hash(self._items)

    def get(
        self,
        key: PeriodicLinkKey,
        default: PeriodicLink | None = None,
    ) -> PeriodicLink | None:
        """Return a periodic link by slave entity key."""
        return self._by_key.get(key, default)

    def where(self, *, dimension: int | None = None) -> PeriodicLinkCollection:
        """Return links for one topological dimension."""
        return PeriodicLinkCollection(
            link for link in self if dimension is None or link.dimension == dimension
        )

    def by_dimension(self, dimension: int) -> PeriodicLinkCollection:
        """Return links for one topological dimension."""
        return self.where(dimension=dimension)

    @property
    def keys(self) -> tuple[PeriodicLinkKey, ...]:
        """Slave entity keys in parser order."""
        return tuple(self._by_key)


@dataclass(frozen=True, slots=True)
class PhysicalGroup:
    """A named or anonymous physical group and its resolved mesh contents."""

    dimension: int
    tag: int
    name: str | None
    entities: EntityCollection
    elements: ElementCollection
    nodes: NodeCollection

    @property
    def key(self) -> PhysicalGroupKey:
        """Physical group key as ``(dimension, tag)``."""
        return self.dimension, self.tag


class PhysicalGroupCollection:
    """Physical groups keyed by ``(dimension, tag)`` and unambiguous names."""

    __slots__ = ("_items", "_by_key", "_by_name")

    def __init__(self, items: Iterable[PhysicalGroup]):
        self._items = tuple(items)
        self._by_key = {group.key: group for group in self._items}
        if len(self._by_key) != len(self._items):
            raise ValueError("Physical group keys must be unique")

        self._by_name: dict[str, list[PhysicalGroup]] = {}
        for group in self._items:
            if group.name is not None:
                self._by_name.setdefault(group.name, []).append(group)

    def __iter__(self) -> Iterator[PhysicalGroup]:
        return iter(self._items)

    def __len__(self) -> int:
        return len(self._items)

    def __getitem__(self, key: PhysicalGroupKey | str) -> PhysicalGroup:
        if isinstance(key, str):
            matches = self._by_name.get(key, ())
            if len(matches) == 1:
                return matches[0]
            if not matches:
                raise KeyError(key)
            raise KeyError(
                f"Physical group name {key!r} is ambiguous; use (dimension, tag)"
            )
        return self._by_key[key]

    def __contains__(self, value: object) -> bool:
        if isinstance(value, str):
            return value in self._by_name
        if isinstance(value, tuple) and len(value) == 2:
            return value in self._by_key
        return value in self._items

    def __repr__(self) -> str:
        return f"PhysicalGroupCollection({list(self._items)!r})"

    def get(
        self,
        key: PhysicalGroupKey | str,
        default: PhysicalGroup | None = None,
    ) -> PhysicalGroup | None:
        """Return a physical group, or *default* only when the key is absent.

        Ambiguous names still raise :class:`KeyError`; callers must use the
        explicit ``(dimension, tag)`` key in that case.
        """
        if isinstance(key, str):
            matches = self._by_name.get(key, ())
            if len(matches) == 1:
                return matches[0]
            if not matches:
                return default
            raise KeyError(
                f"Physical group name {key!r} is ambiguous; use (dimension, tag)"
            )
        return self._by_key.get(key, default)

    def where(self, *, dimension: int | None = None) -> PhysicalGroupCollection:
        """Return physical groups of the selected dimension."""
        return PhysicalGroupCollection(
            group for group in self if dimension is None or group.dimension == dimension
        )

    def by_dimension(self, dimension: int) -> PhysicalGroupCollection:
        """Return physical groups of one topological dimension."""
        return self.where(dimension=dimension)

    @property
    def keys(self) -> tuple[PhysicalGroupKey, ...]:
        """Physical group keys in parser order."""
        return tuple(self._by_key)

    @property
    def names(self) -> tuple[str, ...]:
        """Declared physical group names in parser order."""
        return tuple(group.name for group in self if group.name is not None)


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
    physical_groups: PhysicalGroupCollection
    periodic_links: PeriodicLinkCollection = field(
        default_factory=lambda: PeriodicLinkCollection(())
    )

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
                    physical_tags=mesh.get_entity_physical_tags(*key),
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
            entity_physical_tags = mesh.get_entity_physical_tags(*key)

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

                element_physical_tags = mesh.get_element_physical_tags(
                    legacy_element.get_tag()
                )
                if not element_physical_tags:
                    element_physical_tags = entity_physical_tags

                element = Element(
                    tag=legacy_element.get_tag(),
                    element_type=element_type,
                    nodes=tuple(element_nodes),
                    dimension=key[0],
                    entity_tag=key[1],
                    physical_tags=element_physical_tags,
                )
                entity_elements.append(element)
                all_elements.append(element)

        elements = ElementCollection(all_elements)
        entity_keys = dict.fromkeys(
            [
                *mesh.get_entity_physical_assignments(),
                *nodes_by_entity,
                *elements_by_entity,
            ]
        )
        entity_values: list[Entity] = []

        for dimension, tag in entity_keys:
            key = dimension, tag
            entity_elements = ElementCollection(elements_by_entity.get(key, ()))
            physical_tags = list(mesh.get_entity_physical_tags(*key))
            for element in entity_elements:
                for physical_tag in element.physical_tags:
                    if physical_tag not in physical_tags:
                        physical_tags.append(physical_tag)

            entity_values.append(
                Entity(
                    dimension=dimension,
                    tag=tag,
                    nodes=NodeCollection(nodes_by_entity.get(key, ())),
                    elements=entity_elements,
                    physical_tags=tuple(physical_tags),
                )
            )

        entities = EntityCollection(entity_values)
        physical_names = mesh.get_physical_names()
        physical_keys = dict.fromkeys(physical_names)

        for entity in entities:
            for physical_tag in entity.physical_tags:
                physical_keys.setdefault((entity.dimension, physical_tag), None)
        for element in elements:
            for physical_tag in element.physical_tags:
                physical_keys.setdefault((element.dimension, physical_tag), None)

        physical_group_values: list[PhysicalGroup] = []
        for dimension, physical_tag in physical_keys:
            group_entities = entities.where(
                dimension=dimension,
                physical_tag=physical_tag,
            )
            group_elements = elements.where(
                dimension=dimension,
                physical_tag=physical_tag,
            )
            node_tags = {node.tag for entity in group_entities for node in entity.nodes}
            node_tags.update(
                node.tag for element in group_elements for node in element.nodes
            )
            physical_group_values.append(
                PhysicalGroup(
                    dimension=dimension,
                    tag=physical_tag,
                    name=physical_names.get((dimension, physical_tag)),
                    entities=group_entities,
                    elements=group_elements,
                    nodes=NodeCollection(
                        node for node in nodes if node.tag in node_tags
                    ),
                )
            )

        physical_groups = PhysicalGroupCollection(physical_group_values)

        periodic_links = PeriodicLinkCollection(
            PeriodicLink(
                dimension=dimension,
                entity_tag=entity_tag,
                master_entity_tag=master_entity_tag,
                affine_transform=affine_transform,
                node_pairs=node_pairs,
            )
            for (
                dimension,
                entity_tag,
                master_entity_tag,
                affine_transform,
                node_pairs,
            ) in mesh.get_periodic_links()
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
            physical_groups=physical_groups,
            periodic_links=periodic_links,
        )

    def entity(self, dimension: int, tag: int) -> Entity:
        """Return one elementary entity without constructing a tuple key."""
        return self.entities[(dimension, tag)]

    def physical_group(
        self,
        name_or_tag: str | int,
        *,
        dimension: int | None = None,
    ) -> PhysicalGroup:
        """Return a physical group by name or by tag and dimension."""
        if isinstance(name_or_tag, str):
            return self.physical_groups[name_or_tag]
        if dimension is None:
            matches = [
                group for group in self.physical_groups if group.tag == name_or_tag
            ]
            if len(matches) == 1:
                return matches[0]
            if not matches:
                raise KeyError(name_or_tag)
            raise KeyError(
                f"Physical tag {name_or_tag} exists in multiple dimensions; "
                "provide dimension="
            )
        return self.physical_groups[(dimension, name_or_tag)]

    def periodic_link(self, dimension: int, tag: int) -> PeriodicLink:
        """Return the periodic relation for one slave entity."""
        return self.periodic_links[(dimension, tag)]

    @property
    def points(self) -> EntityCollection:
        """Zero-dimensional entities."""
        return self.entities.by_dimension(0)

    @property
    def curves(self) -> EntityCollection:
        """One-dimensional entities."""
        return self.entities.by_dimension(1)

    @property
    def surfaces(self) -> EntityCollection:
        """Two-dimensional entities."""
        return self.entities.by_dimension(2)

    @property
    def volumes(self) -> EntityCollection:
        """Three-dimensional entities."""
        return self.entities.by_dimension(3)

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
            f"nodes={len(self.nodes)}, elements={len(self.elements)}, "
            f"physical_groups={len(self.physical_groups)}, "
            f"periodic_links={len(self.periodic_links)})"
        )

    __str__ = __repr__


def read(
    source: str | os.PathLike[str] | TextIO,
    *,
    name: str | None = None,
) -> Mesh:
    """Read a path or text stream into the modern API.

    Top-level :func:`gmshparser.parse` intentionally retains the mutable
    compatibility API. Within :mod:`gmshparser.api`, :func:`parse` is an alias
    for this modern reader.
    """
    if hasattr(source, "read"):
        stream = cast(TextIO, source)
        mesh_name = name or str(getattr(stream, "name", "<stream>"))
        return _read_stream(stream, mesh_name)

    path = os.fspath(source)
    with open(path, encoding="utf-8") as stream:
        return _read_stream(stream, name or path)


def parse(
    source: str | os.PathLike[str] | TextIO,
    *,
    name: str | None = None,
) -> Mesh:
    """Parse into the modern model inside the explicit ``gmshparser.api`` namespace."""
    return read(source, name=name)


def _read_stream(stream: TextIO, name: str) -> Mesh:
    from .modern_builder import ModernMeshBuilder

    builder = ModernMeshBuilder(name)
    MainParser().parse(builder, stream)
    return builder.build()
