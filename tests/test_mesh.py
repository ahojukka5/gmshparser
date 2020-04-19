from gmshparser.mesh import Mesh


def test_mesh():
    m = Mesh()
    m.set_version(4.1)
    m.set_ascii(True)
    m.set_precision(8)
    m.set_min_node_tag(1)
    m.set_max_node_tag(3)
    m.set_number_of_entities(1)
    m.set_number_of_nodes(3)
    assert m.get_version() == 4.1
    assert m.get_ascii() is True
    assert m.get_precision() == 8
    assert m.get_min_node_tag() == 1
    assert m.get_max_node_tag() == 3
    assert m.get_number_of_entities() == 1
    assert m.get_number_of_nodes() == 3
