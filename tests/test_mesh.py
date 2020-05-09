from gmshparser.mesh import Mesh

str_expected = """
Mesh name: testmesh.msh
Mesh version: 4.1
Number of nodes: 3
Minimum node tag: 1
Maximum node tag: 3
Number of node entities: 1
Number of elements: 2
Minimum element tag: 1
Maximum element tag: 2
Number of element entities: 1
"""


def test_mesh():
    m = Mesh()
    m.set_name("testmesh.msh")
    m.set_version(4.1)
    m.set_ascii(True)
    m.set_precision(8)
    m.set_min_node_tag(1)
    m.set_max_node_tag(3)
    m.set_number_of_node_entities(1)
    m.set_number_of_nodes(3)
    m.set_min_element_tag(1)
    m.set_max_element_tag(2)
    m.set_number_of_element_entities(1)
    m.set_number_of_elements(2)
    assert m.get_name() == "testmesh.msh"
    assert m.get_version() == 4.1
    assert m.get_ascii() is True
    assert m.get_precision() == 8
    assert m.get_min_node_tag() == 1
    assert m.get_max_node_tag() == 3
    assert m.get_number_of_node_entities() == 1
    assert m.get_number_of_nodes() == 3
    assert m.__str__() == str_expected.strip()
    assert len(m.get_element_entities()) == 0
    assert len(m.get_node_entities()) == 0
