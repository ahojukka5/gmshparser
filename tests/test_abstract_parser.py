import pytest
from gmshparser.abstract_parser import AbstractParser


def test_abstract_parser():
    with pytest.raises(NotImplementedError):
        AbstractParser.get_section_name()
    p = AbstractParser()
    with pytest.raises(NotImplementedError):
        p.parse(1, 2)
