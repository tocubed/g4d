from csg import *
import numpy as np

_cube_points = np.array([[-0.5, -0.5, -0.5],
                         [-0.5, -0.5,  0.5],
                         [-0.5,  0.5, -0.5],
                         [-0.5,  0.5,  0.5],
                         [ 0.5, -0.5, -0.5],
                         [ 0.5, -0.5,  0.5],
                         [ 0.5,  0.5, -0.5],
                         [ 0.5,  0.5,  0.5]])

def hypercube():
    polytopes = []

    plane = Plane(np.zeros(4), 0.5)
    cube = ConvexPolytope([Vertex(p) for p in _cube_points], plane)

    for i in range(8):
        face = cube.clone()
        face.plane.normal[i % 4] = -1.0 if i // 4 else 1.0

        polytopes.append(face)

    return CSG(polytopes)
