from gmshparser.element_entity import ElementEntity


class ElementMock(object):
    def __init__(self):
        pass

    def get_tag(self):
        return 42


__expected_str__ = """
---- Element entity # 1 ----
Dimension: 2
Element type: 3
Number of elements: 1
"""


def test_element_entity():
    ee = ElementEntity()
    ee.set_dimension(2)
    ee.set_tag(1)
    ee.set_number_of_elements(1)
    ee.set_element_type(3)
    element = ElementMock()
    ee.add_element(element)
    assert ee.get_dimension() == 2
    assert ee.get_tag() == 1
    assert ee.get_number_of_elements() == 1
    assert ee.get_element_type() == 3
    assert ee.get_element(42) == element
    assert len(ee.get_elements()) == 1
    assert ee.__str__() == __expected_str__.lstrip()
