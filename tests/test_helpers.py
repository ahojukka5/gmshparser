import gmshparser
import io
import pytest

def test_parse_ints():
    s = io.StringIO("1 2 3 4")
    assert gmshparser.parse_ints(s) == [1, 2, 3, 4]

def test_parse_floats():
    s = io.StringIO("1.1 2.2 3.3 4.4")
    assert gmshparser.parse_floats(s) == [1.1, 2.2, 3.3, 4.4]