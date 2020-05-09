import sys
import argparse
from . import parse

"""gmshparser cli provides some helpers to convert mesh to another format."""


def info(mesh, file):
    print("---- MESH SUMMARY ----", file=file)
    print(mesh, file=file)


def nodes(mesh, file):
    print(mesh.get_number_of_nodes(), file=file)
    for entity in mesh.get_node_entities():
        for node in entity.get_nodes():
            nid = node.get_tag()
            x, y, z = node.get_coordinates()
            print("%d %f %f %f" % (nid, x, y, z), file=file)


def elements(mesh, file):
    print(mesh.get_number_of_elements(), file=file)
    for entity in mesh.get_element_entities():
        eltype = entity.get_element_type()
        for element in entity.get_elements():
            elid = element.get_tag()
            elcon = " ".join(map(str, element.get_connectivity()))
            print("%s %s %s" % (elid, eltype, elcon), file=file)


def main(argv=None, file=sys.stdout):
    parser = argparse.ArgumentParser()
    choices = {"info": info, "nodes": nodes, "elements": elements}
    parser.add_argument('filename', action='store')
    parser.add_argument('action', choices=list(choices.keys()))
    args = parser.parse_args(argv or sys.argv[1:])
    mesh = parse(args.filename)
    choices[args.action](mesh, file)
    return file
