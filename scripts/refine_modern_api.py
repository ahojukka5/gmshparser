from pathlib import Path

path = Path("gmshparser/api.py")
text = path.read_text()


def replace_once(old: str, new: str) -> None:
    global text
    count = text.count(old)
    if count != 1:
        raise RuntimeError(f"Expected one match, found {count}: {old[:80]!r}")
    text = text.replace(old, new, 1)


replace_once(
    '''    "NodeCollection",\n    "Version",\n    "read",\n]''',
    '''    "NodeCollection",\n    "PhysicalGroup",\n    "PhysicalGroupCollection",\n    "PhysicalGroupKey",\n    "Version",\n    "parse",\n    "read",\n]''',
)
replace_once(
    "type EntityKey = tuple[int, int]\n",
    "type EntityKey = tuple[int, int]\ntype PhysicalGroupKey = tuple[int, int]\n",
)
replace_once(
    "    parametric_coordinates: tuple[float, ...] = ()\n",
    "    parametric_coordinates: tuple[float, ...] = ()\n"
    "    physical_tags: tuple[int, ...] = ()\n",
)

replace_once(
    '''@dataclass(frozen=True, slots=True)
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
''',
    '''@dataclass(frozen=True, slots=True)
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
''',
)

replace_once(
    '''class NodeCollection(_TaggedCollection[Node]):
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
''',
    '''class NodeCollection(_TaggedCollection[Node]):
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
''',
)

replace_once(
    '''class ElementCollection(_TaggedCollection[Element]):
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
''',
    '''class ElementCollection(_TaggedCollection[Element]):
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
''',
)

replace_once(
    '''@dataclass(frozen=True, slots=True)
class Entity:
    """A unified Gmsh entity containing both nodes and elements."""

    dimension: int
    tag: int
    nodes: NodeCollection
    elements: ElementCollection
''',
    '''@dataclass(frozen=True, slots=True)
class Entity:
    """A unified Gmsh entity containing both nodes and elements."""

    dimension: int
    tag: int
    nodes: NodeCollection
    elements: ElementCollection
    physical_tags: tuple[int, ...] = ()
''',
)
replace_once(
    '''        has_nodes: bool | None = None,
        has_elements: bool | None = None,
    ) -> EntityCollection:
''',
    '''        has_nodes: bool | None = None,
        has_elements: bool | None = None,
        physical_tag: int | None = None,
    ) -> EntityCollection:
''',
)
replace_once(
    '''            and (has_elements is None or bool(entity.elements) is has_elements)
            and (wanted_type is None or wanted_type in entity.element_types)
        )

    @property
''',
    '''            and (has_elements is None or bool(entity.elements) is has_elements)
            and (wanted_type is None or wanted_type in entity.element_types)
            and (physical_tag is None or physical_tag in entity.physical_tags)
        )

    def by_dimension(self, dimension: int) -> EntityCollection:
        """Return entities of one topological dimension."""
        return self.where(dimension=dimension)

    @property
''',
)

physical_classes = '''

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
        """Return a physical group by key or unambiguous name."""
        try:
            return self[key]
        except KeyError:
            return default

    def where(self, *, dimension: int | None = None) -> PhysicalGroupCollection:
        """Return physical groups of the selected dimension."""
        return PhysicalGroupCollection(
            group
            for group in self
            if dimension is None or group.dimension == dimension
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
'''
replace_once(
    "\n\n@dataclass(frozen=True, slots=True)\nclass Mesh:\n",
    physical_classes + "\n\n@dataclass(frozen=True, slots=True)\nclass Mesh:\n",
)
replace_once(
    '''    elements: ElementCollection
    entities: EntityCollection
''',
    '''    elements: ElementCollection
    entities: EntityCollection
    physical_groups: PhysicalGroupCollection
''',
)
replace_once(
    '''                    entity_tag=key[1],
                    parametric_coordinates=raw_coordinates[3:],
                )
''',
    '''                    entity_tag=key[1],
                    parametric_coordinates=raw_coordinates[3:],
                    physical_tags=mesh.get_entity_physical_tags(*key),
                )
''',
)
replace_once(
    '''            entity_elements = elements_by_entity.setdefault(key, [])
            element_type = ElementType(legacy_entity.get_element_type())

            for legacy_element in legacy_entity.get_elements():
''',
    '''            entity_elements = elements_by_entity.setdefault(key, [])
            element_type = ElementType(legacy_entity.get_element_type())
            entity_physical_tags = mesh.get_entity_physical_tags(*key)

            for legacy_element in legacy_entity.get_elements():
''',
)
replace_once(
    '''                element = Element(
                    tag=legacy_element.get_tag(),
                    type=element_type,
                    nodes=tuple(element_nodes),
                    dimension=key[0],
                    entity_tag=key[1],
                )
''',
    '''                element_physical_tags = mesh.get_element_physical_tags(
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
''',
)
replace_once(
    '''        elements = ElementCollection(all_elements)
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
''',
    '''        elements = ElementCollection(all_elements)
        entity_keys = dict.fromkeys([*nodes_by_entity, *elements_by_entity])
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
            node_tags = {
                node.tag for entity in group_entities for node in entity.nodes
            }
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

        major = mesh.get_version_major()
''',
)
replace_once(
    '''            elements=elements,
            entities=entities,
        )

    @property
    def dimension(self) -> int | None:
''',
    '''            elements=elements,
            entities=entities,
            physical_groups=physical_groups,
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
''',
)
replace_once(
    '''            f"Mesh(name={self.name!r}, version={version!r}, "
            f"nodes={len(self.nodes)}, elements={len(self.elements)})"
''',
    '''            f"Mesh(name={self.name!r}, version={version!r}, "
            f"nodes={len(self.nodes)}, elements={len(self.elements)}, "
            f"physical_groups={len(self.physical_groups)})"
''',
)
replace_once(
    '''    Use :func:`gmshparser.parse` when the mutable compatibility API is required.
    """
''',
    '''    Top-level :func:`gmshparser.parse` intentionally retains the mutable
    compatibility API. Within :mod:`gmshparser.api`, :func:`parse` is an alias
    for this modern reader.
    """
''',
)
replace_once(
    '''

def _read_stream(stream: TextIO, name: str) -> Mesh:
''',
    '''

def parse(
    source: str | os.PathLike[str] | TextIO,
    *,
    name: str | None = None,
) -> Mesh:
    """Parse into the modern model inside the explicit ``gmshparser.api`` namespace."""
    return read(source, name=name)


def _read_stream(stream: TextIO, name: str) -> Mesh:
''',
)

path.write_text(text)
