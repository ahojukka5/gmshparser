from gmshparser.elements_parser import ElementsParser
from gmshparser.mesh import Mesh
from io import StringIO

__content__ = """
$Elements
1 2 1 2
2 1 3 2
1 1 2 3 4
2 2 5 6 3
$EndElements
"""


def test_elements_parser():
    parser = ElementsParser()
    mesh = Mesh()
    data = StringIO(__content__.strip())
    parser.parse(mesh, data)

    assert mesh.get_number_of_elements() == 2
    assert mesh.get_min_element_tag() == 1
    assert mesh.get_max_element_tag() == 2
    assert mesh.has_element_entity(1)

    entity = mesh.get_element_entity(1)
    assert entity.get_tag() == 1
    assert entity.get_dimension() == 2
    assert entity.get_element_type() == 3
    assert entity.get_number_of_elements() == 2

    assert entity.get_element(1).get_tag() == 1
    assert entity.get_element(1).get_connectivity() == [1, 2, 3, 4]
    assert entity.get_element(2).get_tag() == 2
    assert entity.get_element(2).get_connectivity() == [2, 5, 6, 3]
