"""Example: Visualize quadrilateral mesh using matplotlib.

This example demonstrates how to visualize a mesh containing quadrilateral
elements using gmshparser and matplotlib.
"""

import gmshparser
import matplotlib.pyplot as plt
import matplotlib.patches as patches


def visualize_quads_simple():
    """Simple quad visualization using get_quads()."""
    # Parse mesh file
    mesh = gmshparser.parse("../data/testmesh_v2_0.msh")
    
    # Extract quad elements
    X, Y, Q = gmshparser.helpers.get_quads(mesh)
    
    # Create figure
    fig, ax = plt.subplots(figsize=(8, 6))
    
    # Plot each quad as a polygon
    for quad in Q:
        coords = [[X[i], Y[i]] for i in quad]
        coords.append(coords[0])  # Close the polygon
        xs, ys = zip(*coords)
        ax.plot(xs, ys, 'k-', linewidth=1.5)
    
    # Plot nodes
    ax.plot(X, Y, 'ro', markersize=8)
    
    # Add node labels
    for i, (x, y) in enumerate(zip(X, Y)):
        ax.text(x, y, f' {i}', fontsize=10, verticalalignment='bottom')
    
    ax.set_aspect('equal')
    ax.set_title('Quadrilateral Mesh Visualization')
    ax.set_xlabel('X')
    ax.set_ylabel('Y')
    ax.grid(True, alpha=0.3)
    plt.tight_layout()
    plt.savefig('quad_mesh_simple.png', dpi=150)
    print("Saved: quad_mesh_simple.png")


def visualize_mixed_mesh():
    """Visualize mesh with both triangles and quads."""
    # Parse mesh file
    mesh = gmshparser.parse("../data/test_from_internet/mixed_v2_0.msh")
    
    # Extract all 2D elements
    data = gmshparser.helpers.get_elements_2d(mesh)
    nodes = data['nodes']
    
    # Create figure
    fig, ax = plt.subplots(figsize=(10, 6))
    
    # Plot triangles in blue
    for tri in data['triangles']:
        coords = [(nodes[nid][0], nodes[nid][1]) for nid in tri]
        coords.append(coords[0])  # Close the polygon
        xs, ys = zip(*coords)
        ax.plot(xs, ys, 'b-', linewidth=1.5, label='Triangle' if tri == data['triangles'][0] else '')
    
    # Plot quads in red
    for quad in data['quads']:
        coords = [(nodes[nid][0], nodes[nid][1]) for nid in quad]
        coords.append(coords[0])  # Close the polygon
        xs, ys = zip(*coords)
        ax.plot(xs, ys, 'r-', linewidth=1.5, label='Quad' if quad == data['quads'][0] else '')
    
    # Plot nodes
    X = [nodes[nid][0] for nid in data['node_ids']]
    Y = [nodes[nid][1] for nid in data['node_ids']]
    ax.plot(X, Y, 'ko', markersize=6)
    
    ax.set_aspect('equal')
    ax.set_title('Mixed Mesh: Triangles and Quadrilaterals')
    ax.set_xlabel('X')
    ax.set_ylabel('Y')
    ax.grid(True, alpha=0.3)
    ax.legend()
    plt.tight_layout()
    plt.savefig('mixed_mesh.png', dpi=150)
    print("Saved: mixed_mesh.png")


if __name__ == "__main__":
    print("Visualizing quadrilateral mesh...")
    visualize_quads_simple()
    
    print("\nVisualizing mixed mesh...")
    visualize_mixed_mesh()
    
    print("\nDone! Check the generated PNG files.")
