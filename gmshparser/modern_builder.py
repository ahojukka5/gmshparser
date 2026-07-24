from __future__ import annotations

from dataclasses import dataclass
from typing import TYPE_CHECKING

from .element_types import ElementType
from .errors import InvalidMeshError

if TYPE_CHECKING:
    from .api import Mesh
    from .element_entity import ElementEntity
    from .node_entity import NodeEntity


type EntityKey = tuple[int, int]
type PhysicalGroupKey = tuple[int, int]


@dataclass(frozen=True, slots=True)
class _RawNode:
    tag: int
    coordinates: tuple[float, ...]
    dimension: int
    entity_tag: int


@dataclass(frozen=True, slots=True)
class _RawElement:
    tag: int
    node_tags: tuple[int, ...]


@dataclass(frozen=True, slots=True)
class _RawElementBlock:
    dimension: int
    entity_tag: int
    element_type: int
    elements: tuple[_RawElement, ...]


class ModernMeshBuilder:
    """Parser target that builds the immutable API without a legacy mesh.

    Existing section parsers populate this object through the same small mutable
    protocol used by the compatibility :class:`gmshparser.mesh.Mesh`. Incoming
    legacy node and element block objects are immediately flattened into compact
    immutable records; the compatibility mesh itself is never constructed.
    """

    def __init__(self, name: str = "New Mesh"):
        self._name = name
        self._version: float | None = None
        self._version_major: int | None = None
        self._version_minor: int | None = None
        self._ascii = True
        self._precision = 8

        self._number_of_node_entities = 0
        self._number_of_nodes = 0
        self._min_node_tag = 0
        self._max_node_tag = 0
        self._number_of_element_entities = 0
        self._number_of_elements = 0
        self._min_element_tag = 0
        self._max_element_tag = 0

        self._raw_nodes: list[_RawNode] = []
        self._raw_element_blocks: list[_RawElementBlock] = []
        self._physical_names: dict[PhysicalGroupKey, str] = {}
        self._entity_physical_tags: dict[EntityKey, tuple[int, ...]] = {}
        self._element_physical_tags: dict[int, tuple[int, ...]] = {}

    def set_name(self, name: str) -> None:
        self._name = name

    def get_name(self) -> str:
        return self._name

    def set_version(self, version: float) -> None:
        self._version = version
        major = int(version)
        self._version_major = major
        self._version_minor = int(round((version - major) * 10))

    def get_version(self) -> float | None:
        return self._version

    def get_version_major(self) -> int | None:
        return self._version_major

    def get_version_minor(self) -> int | None:
        return self._version_minor

    def set_ascii(self, is_ascii: bool) -> None:
        self._ascii = is_ascii

    def get_ascii(self) -> bool:
        return self._ascii

    def set_precision(self, precision: int) -> None:
        self._precision = precision

    def get_precision(self) -> int:
        return self._precision

    def set_number_of_node_entities(self, value: int) -> None:
        self._number_of_node_entities = value

    def get_number_of_node_entities(self) -> int:
        return self._number_of_node_entities

    def set_number_of_nodes(self, value: int) -> None:
        self._number_of_nodes = value

    def get_number_of_nodes(self) -> int:
        return self._number_of_nodes

    def set_min_node_tag(self, value: int) -> None:
        self._min_node_tag = value

    def get_min_node_tag(self) -> int:
        return self._min_node_tag

    def set_max_node_tag(self, value: int) -> None:
        self._max_node_tag = value

    def get_max_node_tag(self) -> int:
        return self._max_node_tag

    def set_number_of_element_entities(self, value: int) -> None:
        self._number_of_element_entities = value

    def get_number_of_element_entities(self) -> int:
        return self._number_of_element_entities

    def set_number_of_elements(self, value: int) -> None:
        self._number_of_elements = value

    def get_number_of_elements(self) -> int:
        return self._number_of_elements

    def set_min_element_tag(self, value: int) -> None:
        self._min_element_tag = value

    def get_min_element_tag(self) -> int:
        return self._min_element_tag

    def set_max_element_tag(self, value: int) -> None:
        self._max_element_tag = value

    def get_max_element_tag(self) -> int:
        return self._max_element_tag

    def add_node_entity(self, node_entity: NodeEntity) -> None:
        dimension = node_entity.get_dimension()
        entity_tag = node_entity.get_tag()
        for legacy_node in node_entity.get_nodes():
            coordinates = tuple(legacy_node.get_coordinates())
            if len(coordinates) < 3:
                raise InvalidMeshError(
                    f"Node {legacy_node.get_tag()} has fewer than three coordinates"
                )
            self._raw_nodes.append(
                _RawNode(
                    tag=legacy_node.get_tag(),
                    coordinates=coordinates,
                    dimension=dimension,
                    entity_tag=entity_tag,
                )
            )

    def add_element_entity(self, element_entity: ElementEntity) -> None:
        elements = tuple(
            _RawElement(
                tag=legacy_element.get_tag(),
                node_tags=tuple(legacy_element.get_connectivity()),
            )
            for legacy_element in element_entity.get_elements()
        )
        self._raw_element_blocks.append(
            _RawElementBlock(
                dimension=element_entity.get_dimension(),
                entity_tag=element_entity.get_tag(),
                element_type=element_entity.get_element_type(),
                elements=elements,
            )
        )

    def set_physical_name(self, dimension: int, tag: int, name: str) -> None:
        self._physical_names[(dimension, tag)] = name

    def get_physical_names(self) -> dict[PhysicalGroupKey, str]:
        return dict(self._physical_names)

    def set_entity_physical_tags(
        self,
        dimension: int,
        tag: int,
        physical_tags,
    ) -> None:
        self._entity_physical_tags[(dimension, tag)] = self._normalize_tags(
            physical_tags
        )

    def add_entity_physical_tags(
        self,
        dimension: int,
        tag: int,
        physical_tags,
    ) -> None:
        key = dimension, tag
        existing = self._entity_physical_tags.get(key, ())
        self._entity_physical_tags[key] = self._normalize_tags(
            (*existing, *physical_tags)
        )

    def get_entity_physical_tags(
        self,
        dimension: int,
        tag: int,
    ) -> tuple[int, ...]:
        return self._entity_physical_tags.get((dimension, tag), ())

    def set_element_physical_tags(self, element_tag: int, physical_tags) -> None:
        self._element_physical_tags[element_tag] = self._normalize_tags(physical_tags)

    def get_element_physical_tags(self, element_tag: int) -> tuple[int, ...]:
        return self._element_physical_tags.get(element_tag, ())

    def build(self) -> Mesh:
        """Resolve raw parser records into the immutable modern mesh model."""
        from .api import (
            Element,
            ElementCollection,
            Entity,
            EntityCollection,
            Mesh,
            Node,
            NodeCollection,
            PhysicalGroup,
            PhysicalGroupCollection,
            Version,
        )

        nodes_by_entity: dict[EntityKey, list[Node]] = {}
        nodes_by_tag: dict[int, Node] = {}
        all_nodes: list[Node] = []

        for raw_node in self._raw_nodes:
            if raw_node.tag in nodes_by_tag:
                raise InvalidMeshError(f"Duplicate node tag {raw_node.tag}")
            key = raw_node.dimension, raw_node.entity_tag
            node = Node(
                tag=raw_node.tag,
                coordinates=(
                    raw_node.coordinates[0],
                    raw_node.coordinates[1],
                    raw_node.coordinates[2],
                ),
                dimension=raw_node.dimension,
                entity_tag=raw_node.entity_tag,
                parametric_coordinates=raw_node.coordinates[3:],
                physical_tags=self.get_entity_physical_tags(*key),
            )
            nodes_by_tag[node.tag] = node
            nodes_by_entity.setdefault(key, []).append(node)
            all_nodes.append(node)

        if len(all_nodes) != self._number_of_nodes:
            raise InvalidMeshError(
                f"Mesh declares {self._number_of_nodes} nodes, built {len(all_nodes)}"
            )

        nodes = NodeCollection(all_nodes)
        elements_by_entity: dict[EntityKey, list[Element]] = {}
        element_tags: set[int] = set()
        all_elements: list[Element] = []

        for block in self._raw_element_blocks:
            key = block.dimension, block.entity_tag
            entity_elements = elements_by_entity.setdefault(key, [])
            element_type = ElementType(block.element_type)
            entity_physical_tags = self.get_entity_physical_tags(*key)

            for raw_element in block.elements:
                if raw_element.tag in element_tags:
                    raise InvalidMeshError(f"Duplicate element tag {raw_element.tag}")
                try:
                    element_nodes = tuple(
                        nodes_by_tag[node_tag] for node_tag in raw_element.node_tags
                    )
                except KeyError as error:
                    missing_tag = int(error.args[0])
                    raise InvalidMeshError(
                        f"Element {raw_element.tag} references unknown node "
                        f"{missing_tag}"
                    ) from error

                physical_tags = self.get_element_physical_tags(raw_element.tag)
                if not physical_tags:
                    physical_tags = entity_physical_tags

                element = Element(
                    tag=raw_element.tag,
                    element_type=element_type,
                    nodes=element_nodes,
                    dimension=block.dimension,
                    entity_tag=block.entity_tag,
                    physical_tags=physical_tags,
                )
                element_tags.add(element.tag)
                entity_elements.append(element)
                all_elements.append(element)

        if len(all_elements) != self._number_of_elements:
            raise InvalidMeshError(
                f"Mesh declares {self._number_of_elements} elements, "
                f"built {len(all_elements)}"
            )

        elements = ElementCollection(all_elements)
        entity_keys = dict.fromkeys([*nodes_by_entity, *elements_by_entity])
        entity_values: list[Entity] = []

        for dimension, tag in entity_keys:
            key = dimension, tag
            entity_elements = ElementCollection(elements_by_entity.get(key, ()))
            physical_tags = list(self.get_entity_physical_tags(*key))
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
        physical_keys = dict.fromkeys(self._physical_names)
        entities_by_physical: dict[PhysicalGroupKey, list[Entity]] = {}
        elements_by_physical: dict[PhysicalGroupKey, list[Element]] = {}
        node_tags_by_physical: dict[PhysicalGroupKey, set[int]] = {}

        for entity in entities:
            for physical_tag in entity.physical_tags:
                key = entity.dimension, physical_tag
                physical_keys.setdefault(key, None)
                entities_by_physical.setdefault(key, []).append(entity)
                node_tags_by_physical.setdefault(key, set()).update(
                    node.tag for node in entity.nodes
                )

        for element in elements:
            for physical_tag in element.physical_tags:
                key = element.dimension, physical_tag
                physical_keys.setdefault(key, None)
                elements_by_physical.setdefault(key, []).append(element)
                node_tags_by_physical.setdefault(key, set()).update(
                    node.tag for node in element.nodes
                )

        physical_group_values: list[PhysicalGroup] = []
        for dimension, physical_tag in physical_keys:
            key = dimension, physical_tag
            group_node_tags = node_tags_by_physical.get(key, set())
            physical_group_values.append(
                PhysicalGroup(
                    dimension=dimension,
                    tag=physical_tag,
                    name=self._physical_names.get(key),
                    entities=EntityCollection(entities_by_physical.get(key, ())),
                    elements=ElementCollection(elements_by_physical.get(key, ())),
                    nodes=NodeCollection(
                        node for node in nodes if node.tag in group_node_tags
                    ),
                )
            )

        version = (
            None
            if self._version_major is None or self._version_minor is None
            else Version(self._version_major, self._version_minor)
        )
        return Mesh(
            name=self._name,
            version=version,
            is_ascii=self._ascii,
            data_size=self._precision,
            nodes=nodes,
            elements=elements,
            entities=entities,
            physical_groups=PhysicalGroupCollection(physical_group_values),
        )

    @staticmethod
    def _normalize_tags(tags) -> tuple[int, ...]:
        normalized: list[int] = []
        for tag in tags:
            value = int(tag)
            if value > 0 and value not in normalized:
                normalized.append(value)
        return tuple(normalized)
