"""Command-line helpers for inspecting parsed meshes."""

import argparse
import sys

from . import __version__, parse


def info(mesh, file) -> None:
    """Print the mesh summary."""
    print("---- MESH SUMMARY ----", file=file)
    print(mesh, file=file)


def nodes(mesh, file) -> None:
    """Print all nodes in a simple line-oriented format."""
    print(mesh.get_number_of_nodes(), file=file)
    for entity in mesh.get_node_entities():
        for node in entity.get_nodes():
            nid = node.get_tag()
            x, y, z = node.get_coordinates()
            print("%d %f %f %f" % (nid, x, y, z), file=file)


def elements(mesh, file) -> None:
    """Print all elements in a simple line-oriented format."""
    print(mesh.get_number_of_elements(), file=file)
    for entity in mesh.get_element_entities():
        eltype = entity.get_element_type()
        for element in entity.get_elements():
            elid = element.get_tag()
            elcon = " ".join(map(str, element.get_connectivity()))
            print("%s %s %s" % (elid, eltype, elcon), file=file)


def main(argv=None, file=sys.stdout) -> None:
    """Run the gmshparser command-line interface."""
    parser = argparse.ArgumentParser(description="Inspect an ASCII Gmsh MSH file.")
    parser.add_argument(
        "--version", action="version", version=f"%(prog)s {__version__}"
    )
    choices = {"info": info, "nodes": nodes, "elements": elements}
    parser.add_argument("filename")
    parser.add_argument("action", choices=list(choices))
    args = parser.parse_args(sys.argv[1:] if argv is None else argv)
    mesh = parse(args.filename)
    choices[args.action](mesh, file)
