"""Tests for multi-version support."""

import gmshparser
import os
import tempfile


def test_parse_msh_41():
    """Test parsing MSH 4.1 format file."""
    content = """$MeshFormat
4.1 0 8
$EndMeshFormat
$Nodes
1 6 1 6
2 1 0 6
1
2
3
4
5
6
0. 0. 0.
1. 0. 0.
1. 1. 0.
0. 1. 0.
2. 0. 0.
2. 1. 0.
$EndNodes
$Elements
1 2 1 2
2 1 3 2
1 1 2 3 4
2 2 5 6 3
$EndElements
"""

    with tempfile.NamedTemporaryFile(mode="w", suffix=".msh", delete=False) as f:
        f.write(content)
        filename = f.name

    try:
        mesh = gmshparser.parse(filename)
        assert mesh.get_version() == 4.1
        assert mesh.get_version_major() == 4
        assert mesh.get_version_minor() == 1
        assert mesh.get_number_of_nodes() == 6
        assert mesh.get_number_of_elements() == 2
    finally:
        os.unlink(filename)


def test_parse_msh_22():
    """Test parsing MSH 2.2 format file."""
    content = """$MeshFormat
2.2 0 8
$EndMeshFormat
$Nodes
6
1 0.0 0.0 0.0
2 1.0 0.0 0.0
3 1.0 1.0 0.0
4 0.0 1.0 0.0
5 2.0 0.0 0.0
6 2.0 1.0 0.0
$EndNodes
$Elements
2
1 3 2 99 2 1 2 3 4
2 3 2 99 2 2 5 6 3
$EndElements
"""

    with tempfile.NamedTemporaryFile(mode="w", suffix=".msh", delete=False) as f:
        f.write(content)
        filename = f.name

    try:
        mesh = gmshparser.parse(filename)
        assert mesh.get_version() == 2.2
        assert mesh.get_version_major() == 2
        assert mesh.get_version_minor() == 2
        assert mesh.get_number_of_nodes() == 6
        assert mesh.get_number_of_elements() == 2

        # Check nodes are accessible
        node_count = 0
        for entity in mesh.get_node_entities():
            for node in entity.get_nodes():
                node_count += 1
        assert node_count == 6

        # Check elements are accessible
        element_count = 0
        for entity in mesh.get_element_entities():
            for element in entity.get_elements():
                element_count += 1
        assert element_count == 2

    finally:
        os.unlink(filename)


def test_parse_msh_21():
    """Test parsing MSH 2.1 format file."""
    content = """$MeshFormat
2.1 0 8
$EndMeshFormat
$Nodes
6
1 0.0 0.0 0.0
2 1.0 0.0 0.0
3 1.0 1.0 0.0
4 0.0 1.0 0.0
5 2.0 0.0 0.0
6 2.0 1.0 0.0
$EndNodes
$Elements
2
1 3 2 99 2 1 2 3 4
2 3 2 99 2 2 5 6 3
$EndElements
"""

    with tempfile.NamedTemporaryFile(mode="w", suffix=".msh", delete=False) as f:
        f.write(content)
        filename = f.name

    try:
        mesh = gmshparser.parse(filename)
        assert mesh.get_version() == 2.1
        assert mesh.get_version_major() == 2
        assert mesh.get_version_minor() == 1
        assert mesh.get_number_of_nodes() == 6
        assert mesh.get_number_of_elements() == 2
    finally:
        os.unlink(filename)


def test_parse_msh_20():
    """Test parsing MSH 2.0 format file."""
    content = """$MeshFormat
2.0 0 8
$EndMeshFormat
$Nodes
6
1 0.0 0.0 0.0
2 1.0 0.0 0.0
3 1.0 1.0 0.0
4 0.0 1.0 0.0
5 2.0 0.0 0.0
6 2.0 1.0 0.0
$EndNodes
$Elements
2
1 3 2 99 2 1 2 3 4
2 3 2 99 2 2 5 6 3
$EndElements
"""

    with tempfile.NamedTemporaryFile(mode="w", suffix=".msh", delete=False) as f:
        f.write(content)
        filename = f.name

    try:
        mesh = gmshparser.parse(filename)
        assert mesh.get_version() == 2.0
        assert mesh.get_version_major() == 2
        assert mesh.get_version_minor() == 0
        assert mesh.get_number_of_nodes() == 6
        assert mesh.get_number_of_elements() == 2
    finally:
        os.unlink(filename)


def test_parse_msh_10():
    """Test parsing MSH 1.0 format file."""
    content = """$NOD
6
1 0.0 0.0 0.0
2 1.0 0.0 0.0
3 1.0 1.0 0.0
4 0.0 1.0 0.0
5 2.0 0.0 0.0
6 2.0 1.0 0.0
$ENDNOD
$ELM
2
1 3 1 1 4 1 2 3 4
2 3 1 1 4 2 5 6 3
$ENDELM
"""

    with tempfile.NamedTemporaryFile(mode="w", suffix=".msh", delete=False) as f:
        f.write(content)
        filename = f.name

    try:
        mesh = gmshparser.parse(filename)
        assert mesh.get_version() == 1.0
        assert mesh.get_version_major() == 1
        assert mesh.get_version_minor() == 0
        assert mesh.get_number_of_nodes() == 6
        assert mesh.get_number_of_elements() == 2
    finally:
        os.unlink(filename)


def test_unsupported_version():
    """Test that unsupported version raises error."""
    content = """$MeshFormat
3.0 0 8
$EndMeshFormat
"""

    with tempfile.NamedTemporaryFile(mode="w", suffix=".msh", delete=False) as f:
        f.write(content)
        filename = f.name

    try:
        try:
            mesh = gmshparser.parse(filename)
            assert False, "Should have raised ValueError"
        except ValueError as e:
            assert "Unrecognized" in str(e) or "not supported" in str(e)
    finally:
        os.unlink(filename)


def test_invalid_version():
    """Test that invalid version raises error."""
    content = """$MeshFormat
99.9 0 8
$EndMeshFormat
"""

    with tempfile.NamedTemporaryFile(mode="w", suffix=".msh", delete=False) as f:
        f.write(content)
        filename = f.name

    try:
        try:
            mesh = gmshparser.parse(filename)
            assert False, "Should have raised ValueError"
        except ValueError as e:
            assert "Unrecognized" in str(e)
    finally:
        os.unlink(filename)
