"""Visualize quadrilateral and mixed 2D meshes with matplotlib."""

from pathlib import Path

import matplotlib.pyplot as plt

import gmshparser

REPOSITORY_ROOT = Path(__file__).resolve().parents[1]
TESTDATA = REPOSITORY_ROOT / "testdata"


def visualize_quads_simple() -> None:
    """Visualize the quadrilateral MSH 2.0 test mesh."""
    mesh = gmshparser.parse(str(TESTDATA / "simple" / "testmesh_v2_0.msh"))
    x_coordinates, y_coordinates, quads = gmshparser.helpers.get_quads(mesh)

    _, axes = plt.subplots(figsize=(8, 6))

    for quad in quads:
        coordinates = [(x_coordinates[index], y_coordinates[index]) for index in quad]
        coordinates.append(coordinates[0])
        x_values, y_values = zip(*coordinates, strict=False)
        axes.plot(x_values, y_values, "k-", linewidth=1.5)

    axes.plot(x_coordinates, y_coordinates, "ro", markersize=8)

    for index, (x_value, y_value) in enumerate(
        zip(x_coordinates, y_coordinates, strict=False)
    ):
        axes.text(
            x_value,
            y_value,
            f" {index}",
            fontsize=10,
            verticalalignment="bottom",
        )

    axes.set_aspect("equal")
    axes.set_title("Quadrilateral Mesh Visualization")
    axes.set_xlabel("X")
    axes.set_ylabel("Y")
    axes.grid(True, alpha=0.3)
    plt.tight_layout()
    plt.savefig("quad_mesh_simple.png", dpi=150)
    print("Saved: quad_mesh_simple.png")


def visualize_mixed_mesh() -> None:
    """Visualize a mesh containing both triangles and quadrilaterals."""
    mesh = gmshparser.parse(
        str(TESTDATA / "complex" / "test_from_internet" / "mixed_v2_0.msh")
    )
    data = gmshparser.helpers.get_elements_2d(mesh)
    nodes = data["nodes"]

    _, axes = plt.subplots(figsize=(10, 6))

    for triangle in data["triangles"]:
        coordinates = [nodes[node_tag] for node_tag in triangle]
        coordinates.append(coordinates[0])
        x_values, y_values = zip(*coordinates, strict=False)
        axes.plot(
            x_values,
            y_values,
            "b-",
            linewidth=1.5,
            label="Triangle" if triangle == data["triangles"][0] else "",
        )

    for quad in data["quads"]:
        coordinates = [nodes[node_tag] for node_tag in quad]
        coordinates.append(coordinates[0])
        x_values, y_values = zip(*coordinates, strict=False)
        axes.plot(
            x_values,
            y_values,
            "r-",
            linewidth=1.5,
            label="Quad" if quad == data["quads"][0] else "",
        )

    x_coordinates = [nodes[node_tag][0] for node_tag in data["node_ids"]]
    y_coordinates = [nodes[node_tag][1] for node_tag in data["node_ids"]]
    axes.plot(x_coordinates, y_coordinates, "ko", markersize=6)

    axes.set_aspect("equal")
    axes.set_title("Mixed Mesh: Triangles and Quadrilaterals")
    axes.set_xlabel("X")
    axes.set_ylabel("Y")
    axes.grid(True, alpha=0.3)
    axes.legend()
    plt.tight_layout()
    plt.savefig("mixed_mesh.png", dpi=150)
    print("Saved: mixed_mesh.png")


if __name__ == "__main__":
    print("Visualizing quadrilateral mesh...")
    visualize_quads_simple()

    print("\nVisualizing mixed mesh...")
    visualize_mixed_mesh()

    print("\nDone! Check the generated PNG files.")
