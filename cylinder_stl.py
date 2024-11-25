import math
from stl import mesh
import numpy as np

# Parameters
outer_radius = 30.0    # Outer cylinder radius in mm
cylinder_height = 130.0
hole_radius = 12.5     # Hole radius in mm
hole_depth = 30.0
segments = 72          # Number of segments (resolution)

# Angles
angle_increment = (2 * math.pi) / segments

# Lists to hold vertices and facets
vertices = []
facets = []

# Function to add a facet
def add_facet(v1, v2, v3):
    facets.append([v1, v2, v3])

# Generate the bottom face of the cylinder
for i in range(segments):
    angle1 = i * angle_increment
    angle2 = (i + 1) % segments * angle_increment

    x1 = outer_radius * math.cos(angle1)
    y1 = outer_radius * math.sin(angle1)
    x2 = outer_radius * math.cos(angle2)
    y2 = outer_radius * math.sin(angle2)

    v0 = [0.0, 0.0, 0.0]  # Center point
    v1 = [x1, y1, 0.0]
    v2 = [x2, y2, 0.0]

    add_facet(v0, v1, v2)

# Generate the side faces of the outer cylinder
for i in range(segments):
    angle1 = i * angle_increment
    angle2 = (i + 1) % segments * angle_increment

    # Bottom vertices
    x1_bottom = outer_radius * math.cos(angle1)
    y1_bottom = outer_radius * math.sin(angle1)
    x2_bottom = outer_radius * math.cos(angle2)
    y2_bottom = outer_radius * math.sin(angle2)

    # Top vertices
    x1_top = x1_bottom
    y1_top = y1_bottom
    x2_top = x2_bottom
    y2_top = y2_bottom

    # Vertices at bottom and top
    v1 = [x1_bottom, y1_bottom, 0.0]
    v2 = [x2_bottom, y2_bottom, 0.0]
    v3 = [x1_top, y1_top, cylinder_height]
    v4 = [x2_top, y2_top, cylinder_height]

    # First triangle
    add_facet(v1, v2, v3)

    # Second triangle
    add_facet(v2, v4, v3)

# Generate the top face (ring) of the cylinder with a hole
for i in range(segments):
    angle1 = i * angle_increment
    angle2 = (i + 1) % segments * angle_increment

    # Outer vertices
    x1_outer = outer_radius * math.cos(angle1)
    y1_outer = outer_radius * math.sin(angle1)
    x2_outer = outer_radius * math.cos(angle2)
    y2_outer = outer_radius * math.sin(angle2)

    # Inner vertices (hole)
    x1_inner = hole_radius * math.cos(angle1)
    y1_inner = hole_radius * math.sin(angle1)
    x2_inner = hole_radius * math.cos(angle2)
    y2_inner = hole_radius * math.sin(angle2)

    z_top = cylinder_height

    # Vertices
    v1 = [x1_outer, y1_outer, z_top]
    v2 = [x2_outer, y2_outer, z_top]
    v3 = [x1_inner, y1_inner, z_top]
    v4 = [x2_inner, y2_inner, z_top]

    # First triangle (outer)
    add_facet(v1, v2, v3)

    # Second triangle (inner)
    add_facet(v2, v4, v3)

# Generate the side walls of the hole
for i in range(segments):
    angle1 = i * angle_increment
    angle2 = (i + 1) % segments * angle_increment

    # Top vertices (at hole radius)
    x1_top = hole_radius * math.cos(angle1)
    y1_top = hole_radius * math.sin(angle1)
    x2_top = hole_radius * math.cos(angle2)
    y2_top = hole_radius * math.sin(angle2)

    # Bottom vertices (at hole depth)
    x1_bottom = x1_top
    y1_bottom = y1_top
    x2_bottom = x2_top
    y2_bottom = y2_top

    z_top = cylinder_height
    z_bottom = cylinder_height - hole_depth

    # Vertices
    v1 = [x1_top, y1_top, z_top]
    v2 = [x2_top, y2_top, z_top]
    v3 = [x1_bottom, y1_bottom, z_bottom]
    v4 = [x2_bottom, y2_bottom, z_bottom]

    # First triangle
    add_facet(v1, v2, v3)

    # Second triangle
    add_facet(v2, v4, v3)

# Generate the bottom face of the hole
for i in range(segments):
    angle1 = i * angle_increment
    angle2 = (i + 1) % segments * angle_increment

    x1 = hole_radius * math.cos(angle1)
    y1 = hole_radius * math.sin(angle1)
    x2 = hole_radius * math.cos(angle2)
    y2 = hole_radius * math.sin(angle2)

    z_bottom = cylinder_height - hole_depth

    v0 = [0.0, 0.0, z_bottom]  # Center point of the hole bottom
    v1 = [x1, y1, z_bottom]
    v2 = [x2, y2, z_bottom]

    # Note the order to ensure the normal faces inward
    add_facet(v0, v2, v1)

# Convert facets to numpy array
facets_np = np.array(facets)

# Create the mesh
cylinder_mesh = mesh.Mesh(np.zeros(facets_np.shape[0], dtype=mesh.Mesh.dtype))
for i, f in enumerate(facets_np):
    for j in range(3):
        cylinder_mesh.vectors[i][j] = f[j]

# Save to file
cylinder_mesh.save('CylinderWithHole.stl')