import pytest
from gmshparser.abstract_parser import AbstractParser


def test_abstract_parser():
    p = AbstractParser()
    with pytest.raises(NotImplementedError):
        p.parse(1, 2)
