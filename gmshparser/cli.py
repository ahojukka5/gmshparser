"""Command-line helpers for inspecting parsed meshes."""

import argparse
import sys
from collections.abc import Callable, Sequence
from typing import TextIO, cast

from . import __version__, parse
from .mesh import Mesh


def info(mesh: Mesh, file: TextIO) -> None:
    """Print the mesh summary."""
    print("---- MESH SUMMARY ----", file=file)
    print(mesh, file=file)


def nodes(mesh: Mesh, file: TextIO) -> None:
    """Print all nodes in a simple line-oriented format."""
    print(mesh.get_number_of_nodes(), file=file)
    for entity in mesh.get_node_entities():
        for node in entity.get_nodes():
            nid = node.get_tag()
            coordinates = node.get_coordinates()
            x, y, z = coordinates[0], coordinates[1], coordinates[2]
            print(f"{nid:d} {x:f} {y:f} {z:f}", file=file)


def elements(mesh: Mesh, file: TextIO) -> None:
    """Print all elements in a simple line-oriented format."""
    print(mesh.get_number_of_elements(), file=file)
    for entity in mesh.get_element_entities():
        eltype = entity.get_element_type()
        for element in entity.get_elements():
            elid = element.get_tag()
            elcon = " ".join(map(str, element.get_connectivity()))
            print(f"{elid} {eltype} {elcon}", file=file)


def main(
    argv: Sequence[str] | None = None,
    file: TextIO = sys.stdout,
) -> None:
    """Run the gmshparser command-line interface."""
    parser = argparse.ArgumentParser(
        prog="gmshparser",
        description="Inspect an ASCII Gmsh MSH file.",
    )
    parser.add_argument(
        "--version",
        action="version",
        version=f"%(prog)s {__version__}",
    )
    choices: dict[str, Callable[[Mesh, TextIO], None]] = {
        "info": info,
        "nodes": nodes,
        "elements": elements,
    }
    parser.add_argument("filename")
    parser.add_argument("action", choices=list(choices))
    args = parser.parse_args(sys.argv[1:] if argv is None else argv)
    filename = cast(str, args.filename)
    action = cast(str, args.action)
    mesh = parse(filename)
    choices[action](mesh, file)
