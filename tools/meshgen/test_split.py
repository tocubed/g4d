from csg import *
import numpy as np

def gauss_random(size, loc=0.0, scale=1.0):
    return np.random.normal(loc, scale, size)

def random_plane(d):
    normal = gauss_random(d)

    normal_norm = np.linalg.norm(normal)
    if normal_norm == 0:
        normal[:] = 0
    else:
        normal /= normal_norm

    distance, = gauss_random(1, scale=10.0)

    return Plane(normal, distance)

def square():
    points = [[-0.5, -0.5], [0.5, -0.5], [-0.5, 0.5], [0.5, 0.5]]
    return ConvexPolytope(points, random_plane(3))

def cube():
    points = [
     [ 0, 0, 0],
     [ -0.5 , -0.5 , -0.5],
     [ -0.5 , -0.5 ,  0.5],
     [ -0.5 ,  0.5 , -0.5],
     [ -0.5 ,  0.5 ,  0.5],
     [  0.5 , -0.5 , -0.5],
     [  0.5 , -0.5 ,  0.5],
     [  0.5 ,  0.5 , -0.5],
     [  0.5 ,  0.5 ,  0.5]]
    vertices = [Vertex(np.array(p)) for p in points]
    return ConvexPolytope(vertices, random_plane(4))

if __name__ == '__main__':
    import sys
    planes, = map(int, sys.argv[1:])

    cube = cube()
    print("cube volume:", cube.volume)

    max_volume_error = 0.0
    for _ in range(planes):
        p = random_plane(4)
        f, b, cf, cb = p.split_polytope(cube)

        if f and b:
            volume_error = f.volume + b.volume - cube.volume
            max_volume_error = max(max_volume_error, volume_error)

    print("maximum volume error:", max_volume_error)
