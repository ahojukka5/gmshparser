from pathlib import Path


def replace(path: str, old: str, new: str, *, count: int = -1) -> None:
    target = Path(path)
    text = target.read_text()
    if old not in text:
        raise RuntimeError(f"Expected text not found in {path}: {old!r}")
    target.write_text(text.replace(old, new, count))


replace(
    "gmshparser/mesh.py",
    "from io import StringIO\n",
    "from collections.abc import ValuesView\nfrom io import StringIO\n",
)
replace(
    "gmshparser/mesh.py",
    "    def get_node_entities(self) -> list[NodeEntity]:\n",
    "    def get_node_entities(self) -> ValuesView[NodeEntity]:\n",
)
replace(
    "gmshparser/mesh.py",
    "    def get_element_entities(self) -> list[ElementEntity]:\n",
    "    def get_element_entities(self) -> ValuesView[ElementEntity]:\n",
)

replace(
    "gmshparser/nodes_parser.py",
    """                for tag in node_tags:
                    coordinates = parse_floats(io)
                    if len(coordinates) != expected_coordinates:
                        raise InvalidNodeError(
                            f"Node {tag} requires {expected_coordinates} coordinate values, "
                            f"got {len(coordinates)}"
                        )
                    records.append((tag, tuple(coordinates)))
""",
    """                for tag in node_tags:
                    coordinate_values = parse_floats(io)
                    if len(coordinate_values) != expected_coordinates:
                        raise InvalidNodeError(
                            f"Node {tag} requires {expected_coordinates} coordinate values, "
                            f"got {len(coordinate_values)}"
                        )
                    records.append((tag, tuple(coordinate_values)))
""",
)

for path in ("gmshparser/elements_parser_v1.py", "gmshparser/elements_parser_v2.py"):
    replace(
        path,
        """        for (dimension, entity_tag), physical_tags in physical_tags_by_entity.items():
            mesh.add_entity_physical_tags(dimension, entity_tag, physical_tags)
        for (dimension, entity_tag, element_type), elements in element_groups.items():
            mesh.add_element_block(dimension, entity_tag, element_type, elements)
""",
        """        for (dimension, entity_tag), entity_physical_tags in physical_tags_by_entity.items():
            mesh.add_entity_physical_tags(
                dimension,
                entity_tag,
                entity_physical_tags,
            )
        for (dimension, entity_tag, type_id), block_elements in element_groups.items():
            mesh.add_element_block(dimension, entity_tag, type_id, block_elements)
""",
    )

replace(
    "gmshparser/main_parser.py",
    "from typing import TextIO\n",
    "from typing import Protocol, TextIO, cast\n",
)
replace(
    "gmshparser/main_parser.py",
    """# Default parsers for MSH 4.x format
""",
    """class ParserTarget(Protocol):
    \"\"\"Mutable target populated by the version-specific section parsers.\"\"\"

    def get_name(self) -> str: ...

    def set_version(self, version: float) -> None: ...

    def get_version(self) -> float | None: ...

    def get_version_major(self) -> int | None: ...


# Default parsers for MSH 4.x format
""",
)
replace(
    "gmshparser/main_parser.py",
    "class MainParser(AbstractParser):\n",
    "class MainParser:\n",
)
replace(
    "gmshparser/main_parser.py",
    "    def parse(self, mesh: Mesh, io: TextIO) -> None:\n",
    "    def parse(self, mesh: ParserTarget, io: TextIO) -> None:\n",
)
replace(
    "gmshparser/main_parser.py",
    "        mesh: Mesh,\n        source: SourceTextIO,\n",
    "        mesh: ParserTarget,\n        source: SourceTextIO,\n",
)
replace(
    "gmshparser/main_parser.py",
    "            parser.parse(mesh, source)\n",
    "            parser.parse(cast(Mesh, mesh), cast(TextIO, source))\n",
)
replace(
    "gmshparser/main_parser.py",
    "    def _get_parsers_for_version(self, mesh: Mesh) -> list[type[AbstractParser]]:\n",
    "    def _get_parsers_for_version(\n        self,\n        mesh: ParserTarget,\n    ) -> list[type[AbstractParser]]:\n",
)

replace(
    "gmshparser/modern_builder.py",
    "            entity_elements = elements_by_entity.setdefault(key, [])\n",
    "            entity_element_values = elements_by_entity.setdefault(key, [])\n",
    count=1,
)
replace(
    "gmshparser/modern_builder.py",
    "                physical_tags = record_physical_tags\n                if not physical_tags:\n                    physical_tags = self.get_element_physical_tags(element_tag)\n                if not physical_tags:\n                    physical_tags = entity_physical_tags\n",
    "                resolved_physical_tags = record_physical_tags\n                if not resolved_physical_tags:\n                    resolved_physical_tags = self.get_element_physical_tags(element_tag)\n                if not resolved_physical_tags:\n                    resolved_physical_tags = entity_physical_tags\n",
)
replace(
    "gmshparser/modern_builder.py",
    "                    physical_tags=physical_tags,\n",
    "                    physical_tags=resolved_physical_tags,\n",
    count=1,
)
replace(
    "gmshparser/modern_builder.py",
    "                entity_elements.append(element)\n",
    "                entity_element_values.append(element)\n",
    count=1,
)
replace(
    "gmshparser/modern_builder.py",
    """            entity_elements = ElementCollection(elements_by_entity.get(key, ()))
            physical_tags = list(self.get_entity_physical_tags(*key))
            for element in entity_elements:
                for physical_tag in element.physical_tags:
                    if physical_tag not in physical_tags:
                        physical_tags.append(physical_tag)
""",
    """            entity_elements = ElementCollection(elements_by_entity.get(key, ()))
            entity_physical_tag_values = list(self.get_entity_physical_tags(*key))
            for element in entity_elements:
                for physical_tag in element.physical_tags:
                    if physical_tag not in entity_physical_tag_values:
                        entity_physical_tag_values.append(physical_tag)
""",
)
replace(
    "gmshparser/modern_builder.py",
    "                    physical_tags=tuple(physical_tags),\n",
    "                    physical_tags=tuple(entity_physical_tag_values),\n",
    count=1,
)

replace(
    "gmshparser/api.py",
    "from typing import TextIO, cast\n",
    "from typing import Protocol, TextIO, cast\n",
)
replace(
    "gmshparser/api.py",
    """class _TaggedCollection[T]:
""",
    """class _Tagged(Protocol):
    tag: int


class _TaggedCollection[T: _Tagged]:
""",
)
replace(
    "gmshparser/api.py",
    """        for legacy_entity in mesh.get_node_entities():
            key = legacy_entity.get_dimension(), legacy_entity.get_tag()
            entity_nodes = nodes_by_entity.setdefault(key, [])

            for legacy_node in legacy_entity.get_nodes():
""",
    """        for legacy_node_entity in mesh.get_node_entities():
            key = legacy_node_entity.get_dimension(), legacy_node_entity.get_tag()
            entity_nodes = nodes_by_entity.setdefault(key, [])

            for legacy_node in legacy_node_entity.get_nodes():
""",
)
replace(
    "gmshparser/api.py",
    """        for legacy_entity in mesh.get_element_entities():
            key = legacy_entity.get_dimension(), legacy_entity.get_tag()
            entity_elements = elements_by_entity.setdefault(key, [])
            element_type = ElementType(legacy_entity.get_element_type())
            entity_physical_tags = mesh.get_entity_physical_tags(*key)

            for legacy_element in legacy_entity.get_elements():
""",
    """        for legacy_element_entity in mesh.get_element_entities():
            key = (
                legacy_element_entity.get_dimension(),
                legacy_element_entity.get_tag(),
            )
            entity_element_values = elements_by_entity.setdefault(key, [])
            element_type = ElementType(legacy_element_entity.get_element_type())
            entity_physical_tags = mesh.get_entity_physical_tags(*key)

            for legacy_element in legacy_element_entity.get_elements():
""",
)
replace(
    "gmshparser/api.py",
    """                    node = nodes.get(node_tag)
                    if node is None:
                        raise ValueError(
                            f"Element {legacy_element.get_tag()} references "
                            f"unknown node {node_tag}"
                        )
                    element_nodes.append(node)
""",
    """                    resolved_node = nodes.get(node_tag)
                    if resolved_node is None:
                        raise ValueError(
                            f"Element {legacy_element.get_tag()} references "
                            f"unknown node {node_tag}"
                        )
                    element_nodes.append(resolved_node)
""",
)
replace(
    "gmshparser/api.py",
    "                entity_elements.append(element)\n",
    "                entity_element_values.append(element)\n",
    count=1,
)

for path in ("docs/developer-guide/test-results.md", "docs/developer-guide/testing.md"):
    replace(
        path,
        "../../testdata/README.md",
        "https://github.com/ahojukka5/gmshparser/blob/master/testdata/README.md",
    )
