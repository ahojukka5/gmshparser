from io import StringIO

import pytest

import gmshparser


@pytest.mark.parametrize(
    ("header", "error_type", "message"),
    [
        (
            "4.1 0",
            gmshparser.InvalidSectionError,
            "must contain version, file type, and data size",
        ),
        (
            "3.0 0 8",
            gmshparser.UnsupportedVersionError,
            "Unrecognized MSH format version",
        ),
        (
            "4.1 1 8",
            gmshparser.UnsupportedBinaryFormatError,
            "Binary MSH files are not supported",
        ),
    ],
)
def test_mesh_format_errors_have_source_context(header, error_type, message):
    source = StringIO(f"$MeshFormat\n{header}\n$EndMeshFormat\n")

    with pytest.raises(error_type, match=message) as caught:
        gmshparser.read(source, name="broken.msh")

    error = caught.value
    assert isinstance(error, ValueError)
    assert error.filename == "broken.msh"
    assert error.line_number == 2
    assert error.section == "$MeshFormat"
    assert error.line == header
    assert str(error).startswith("broken.msh:2 [$MeshFormat]:")


def test_truncated_nodes_raise_unexpected_eof_with_next_line_number():
    source = StringIO(
        "$MeshFormat\n"
        "4.1 0 8\n"
        "$EndMeshFormat\n"
        "$Nodes\n"
        "1 1 1 1\n"
        "0 1 0 1\n"
        "1\n"
    )

    with pytest.raises(gmshparser.UnexpectedEndOfFileError) as caught:
        gmshparser.read(source, name="truncated.msh")

    error = caught.value
    assert error.filename == "truncated.msh"
    assert error.line_number == 8
    assert error.section == "$Nodes"
    assert error.line is None
    assert "while reading a floating-point record" in str(error)


def test_missing_section_end_marker_reports_actual_line():
    source = StringIO(
        "$MeshFormat\n"
        "4.1 0 8\n"
        "$EndMeshFormat\n"
        "$Nodes\n"
        "0 0 0 0\n"
        "$Elements\n"
    )

    with pytest.raises(gmshparser.InvalidSectionError, match="Expected \\$EndNodes") as caught:
        gmshparser.read(source, name="missing-end.msh")

    error = caught.value
    assert error.line_number == 6
    assert error.section == "$Nodes"
    assert error.line == "$Elements"


def test_invalid_connectivity_retains_element_error_type():
    source = StringIO(
        "$MeshFormat\n"
        "2.2 0 8\n"
        "$EndMeshFormat\n"
        "$Nodes\n"
        "4\n"
        "1 0 0 0\n"
        "2 1 0 0\n"
        "3 0 1 0\n"
        "4 1 1 0\n"
        "$EndNodes\n"
        "$Elements\n"
        "1\n"
        "1 2 2 1 1 1 2 3 4\n"
        "$EndElements\n"
    )

    with pytest.raises(gmshparser.InvalidElementConnectivityError) as caught:
        gmshparser.read(source, name="connectivity.msh")

    error = caught.value
    assert error.filename == "connectivity.msh"
    assert error.line_number == 13
    assert error.section == "$Elements"
    assert error.line == "1 2 2 1 1 1 2 3 4"
    assert "requires 3 nodes, got 4" in str(error)


def test_legacy_and_modern_entry_points_share_error_types(tmp_path):
    path = tmp_path / "binary.msh"
    path.write_text(
        "$MeshFormat\n4.1 1 8\n$EndMeshFormat\n",
        encoding="utf-8",
    )

    with pytest.raises(gmshparser.UnsupportedBinaryFormatError):
        gmshparser.parse(str(path))
    with pytest.raises(gmshparser.UnsupportedBinaryFormatError):
        gmshparser.read(path)


def test_parser_does_not_print_failures_to_stdout(capsys):
    source = StringIO("$MeshFormat\ninvalid\n$EndMeshFormat\n")

    with pytest.raises(gmshparser.InvalidSectionError):
        gmshparser.read(source)

    captured = capsys.readouterr()
    assert captured.out == ""
    assert captured.err == ""


def test_empty_input_is_a_structured_value_error():
    with pytest.raises(gmshparser.InvalidSectionError) as caught:
        gmshparser.read(StringIO(""), name="empty.msh")

    assert isinstance(caught.value, ValueError)
    assert caught.value.filename == "empty.msh"
    assert caught.value.line_number is None
