from gmshparser.node_entity import NodeEntity


def test_node_entity():
    ne = NodeEntity()
    ne.set_dimension(2)
    ne.set_tag(1)
    ne.set_number_of_parametric_coordinates(0)
    ne.set_number_of_nodes(1)
    assert ne.get_dimension() == 2
    assert ne.get_tag() == 1
    assert ne.get_number_of_parametric_coordinates() == 0
    assert ne.get_number_of_nodes() == 1
