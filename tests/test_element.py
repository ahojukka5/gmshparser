from gmshparser.element import Element


def test_element():
    element = Element()
    element.set_tag(1)
    element.set_connectivity([1, 2, 3, 4])
    assert element.get_tag() == 1
    assert element.get_connectivity() == [1, 2, 3, 4]
