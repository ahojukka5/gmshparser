from importlib.resources import files


def test_py_typed_marker_is_available():
    assert files("gmshparser").joinpath("py.typed").is_file()
