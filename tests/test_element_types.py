from io import StringIO

import pytest

from gmshparser import (
    Element,
    ElementFamily,
    ElementType,
    InvalidElementConnectivityError,
    UnknownElementTypeError,
)
from gmshparser.element_types import require_element_type
from gmshparser.elements_parser import ElementsParser
from gmshparser.elements_parser_v1 import ElementsParserV1
from gmshparser.elements_parser_v2 import ElementsParserV2
from gmshparser.mesh import Mesh


@pytest.mark.parametrize(
    ("type_id", "dimension", "order", "node_count", "primary_node_count"),
    [
        (1, 1, 1, 2, 2),
        (2, 2, 1, 3, 3),
        (3, 2, 1, 4, 4),
        (4, 3, 1, 4, 4),
        (5, 3, 1, 8, 8),
        (6, 3, 1, 6, 6),
        (7, 3, 1, 5, 5),
        (8, 1, 2, 3, 2),
        (9, 2, 2, 6, 3),
        (10, 2, 2, 9, 4),
        (11, 3, 2, 10, 4),
        (12, 3, 2, 27, 8),
        (13, 3, 2, 18, 6),
        (14, 3, 2, 14, 5),
        (15, 0, 1, 1, 1),
        (16, 2, 2, 8, 4),
        (17, 3, 2, 20, 8),
        (18, 3, 2, 15, 6),
        (19, 3, 2, 13, 5),
        (20, 2, 3, 9, 3),
        (21, 2, 3, 10, 3),
        (22, 2, 4, 12, 3),
        (23, 2, 4, 15, 3),
        (24, 2, 5, 15, 3),
        (25, 2, 5, 21, 3),
        (26, 1, 3, 4, 2),
        (27, 1, 4, 5, 2),
        (28, 1, 5, 6, 2),
        (29, 3, 3, 20, 4),
        (30, 3, 4, 35, 4),
        (31, 3, 5, 56, 4),
        (92, 3, 3, 64, 8),
        (93, 3, 4, 125, 8),
    ],
)
def test_registered_types_expose_one_authoritative_metadata_table(
    type_id,
    dimension,
    order,
    node_count,
    primary_node_count,
):
    element_type = ElementType(type_id)

    assert element_type.is_known is True
    assert element_type.dimension == dimension
    assert element_type.order == order
    assert element_type.node_count == node_count
    assert element_type.primary_node_count == primary_node_count
    assert element_type.is_linear is (order == 1)
    assert element_type.is_high_order is (order > 1)


def test_families_and_incomplete_types_are_descriptive():
    assert ElementType.POINT.family is ElementFamily.POINT
    assert ElementType.TRIANGLE.family is ElementFamily.TRIANGLE
    assert ElementType.QUADRANGLE.family is ElementFamily.QUADRANGLE
    assert ElementType.TETRAHEDRON.family is ElementFamily.TETRAHEDRON
    assert ElementType.HEXAHEDRON.family is ElementFamily.HEXAHEDRON
    assert ElementType.PRISM.family is ElementFamily.PRISM
    assert ElementType.PYRAMID.family is ElementFamily.PYRAMID

    assert ElementType.SECOND_ORDER_QUADRANGLE.is_complete is True
    assert ElementType.SECOND_ORDER_QUADRANGLE_INCOMPLETE.is_complete is False
    assert ElementType.THIRD_ORDER_TRIANGLE.is_complete is True
    assert ElementType.THIRD_ORDER_TRIANGLE_INCOMPLETE.is_complete is False


def test_unknown_numeric_types_remain_representable_but_cannot_be_inferred():
    element_type = ElementType(999)

    assert element_type.name == "TYPE_999"
    assert element_type.info is None
    assert element_type.family is None
    assert element_type.dimension is None
    assert element_type.order is None
    assert element_type.node_count is None
    assert element_type.is_linear is False
    assert element_type.is_high_order is False

    with pytest.raises(UnknownElementTypeError, match="Unknown Gmsh element type 999"):
        require_element_type(element_type)


def test_modern_element_delegates_topology_metadata_to_its_type():
    element = Element(
        tag=1,
        element_type=ElementType.SECOND_ORDER_TRIANGLE,
        nodes=(),
        dimension=2,
        entity_tag=1,
    )

    assert element.family is ElementFamily.TRIANGLE
    assert element.order == 2
    assert element.expected_node_count == 6
    assert element.primary_node_count == 3
    assert element.is_linear is False
    assert element.is_high_order is True
    assert element.is_complete is True


def test_msh1_parser_validates_declared_and_registered_connectivity_sizes():
    mesh = Mesh()

    with pytest.raises(
        InvalidElementConnectivityError,
        match="declares 4 nodes, but the record contains 3",
    ):
        ElementsParserV1.parse(mesh, StringIO("1\n1 2 1 1 4 1 2 3\n"))


def test_msh2_parser_rejects_unknown_types_instead_of_assuming_3d():
    mesh = Mesh()

    with pytest.raises(UnknownElementTypeError, match="Unknown Gmsh element type 999"):
        ElementsParserV2.parse(mesh, StringIO("1\n1 999 0 1 2 3\n"))


def test_msh2_parser_validates_connectivity_against_registry():
    mesh = Mesh()

    with pytest.raises(
        InvalidElementConnectivityError,
        match="3-node triangle .* requires 3 nodes, got 4",
    ):
        ElementsParserV2.parse(mesh, StringIO("1\n1 2 0 1 2 3 4\n"))


def test_msh4_parser_validates_block_dimension_and_connectivity():
    mesh = Mesh()

    with pytest.raises(ValueError, match="has dimension 2.*block declares 3"):
        ElementsParser.parse(mesh, StringIO("1 1 1 1\n3 1 2 1\n1 1 2 3\n"))

    with pytest.raises(
        InvalidElementConnectivityError,
        match="4-node quadrangle .* requires 4 nodes, got 3",
    ):
        ElementsParser.parse(
            Mesh(),
            StringIO("1 1 1 1\n2 1 3 1\n1 1 2 3\n"),
        )
