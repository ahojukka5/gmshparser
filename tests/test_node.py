from gmshparser.node import Node


def test_node_defaults_are_preserved():
    node = Node()

    assert node.get_tag() == -1
    assert node.get_coordinates() == (None, None, None)


def test_node():
    node = Node()
    node.set_tag(1)
    node.set_coordinates((1.0, 2.0, 3.0))
    assert node.get_tag() == 1
    assert node.get_coordinates() == (1.0, 2.0, 3.0)
