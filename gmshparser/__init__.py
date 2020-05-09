from .mesh import Mesh
from .main_parser import MainParser

__version__ = "0.1.5"
__author__ = "Jukka Aho <ahojukka5@gmail.com>"


def parse(filename: str) -> Mesh:
    """Parse Gmsh .msh file and return `Mesh` object."""
    mesh = Mesh()
    mesh.set_name(filename)
    parser = MainParser()
    with open(filename, "r") as io:
        parser.parse(mesh, io)
    return mesh
