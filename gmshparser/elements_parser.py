from typing import TextIO
from .abstract_parser import AbstractParser
from .mesh import Mesh
from .element import Element
from .helpers import parse_ints
from .element_entity import ElementEntity


class ElementsParser(AbstractParser):
    def parse(self, mesh: Mesh, io: TextIO) -> None:
        line = io.readline()
        if line.startswith("$Elements"):
            line = io.readline()
        meta = list(map(int, line.strip().split(" ")))

        mesh.set_number_of_element_entities(meta[0])
        mesh.set_number_of_elements(meta[1])
        mesh.set_min_element_tag(meta[2])
        mesh.set_max_element_tag(meta[3])
        for i in range(mesh.get_number_of_element_entities()):
            emeta = parse_ints(io)
            entity = ElementEntity()
            entity.set_dimension(emeta[0])
            entity.set_tag(emeta[1])
            entity.set_element_type(emeta[2])
            entity.set_number_of_elements(emeta[3])
            for j in range(entity.get_number_of_elements()):
                element_info = parse_ints(io)
                element_tag = element_info[0]
                element_connectivity = element_info[1:]
                element = Element()
                element.set_tag(element_tag)
                element.set_connectivity(element_connectivity)
                entity.add_element(element)
            mesh.add_element_entity(entity)
