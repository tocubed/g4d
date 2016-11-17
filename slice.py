import numpy as np


def cross4d(a, b, c):
    matrix = np.matrix([a, b, c])

    cross = np.array([
                  np.linalg.det(np.delete(matrix, 0, 1)),
                - np.linalg.det(np.delete(matrix, 1, 1)),
                  np.linalg.det(np.delete(matrix, 2, 1)),
                - np.linalg.det(np.delete(matrix, 3, 1))
            ])

    return cross


def normalize4d(a):
    return a / np.linalg.norm(a)


def normal_to_3simplex(vertices):
    e1 = np.subtract(vertices[1], vertices[0])
    e2 = np.subtract(vertices[2], vertices[0])
    e3 = np.subtract(vertices[3], vertices[0])

    return normalize4d(cross4d(e1, e2, e3))


def intersect_xyz(a, b):
    xyz_normal = [0, 0, 0, 1]
    
    a_t = np.dot(xyz_normal, a)
    b_t = np.dot(xyz_normal, b)

    return np.add(b, (b_t / (b_t - a_t)) * np.subtract(a, b))


def slice_xyz_3simplex(vertices):
    t_values = np.array([vertex[3] for vertex in vertices])
    t_sort_i = np.argsort(t_values)

    t_sort_vs = np.array(vertices)[t_sort_i]
    t_values = t_values[t_sort_i]

    if t_values[0] > 0 or 0 > t_values[3]:
        return ("no intersection", [])
    elif t_values[0] < 0 < t_values[1]:
        return ("triangle intersection: first section", [
                intersect_xyz(t_sort_vs[0], t_sort_vs[1]),
                intersect_xyz(t_sort_vs[0], t_sort_vs[2]),
                intersect_xyz(t_sort_vs[0], t_sort_vs[3])
                ])
    elif t_values[2] < 0 < t_values[3]:
        return ("triangle intersection: second section", [
                intersect_xyz(t_sort_vs[0], t_sort_vs[3]),
                intersect_xyz(t_sort_vs[1], t_sort_vs[3]),
                intersect_xyz(t_sort_vs[2], t_sort_vs[3])
                ])
    elif t_values[1] < 0 < t_values[2]:
        return ("quad intersection", [
                intersect_xyz(t_sort_vs[0], t_sort_vs[2]),
                intersect_xyz(t_sort_vs[0], t_sort_vs[3]),
                intersect_xyz(t_sort_vs[1], t_sort_vs[3]),
                intersect_xyz(t_sort_vs[1], t_sort_vs[2])
                ])
    else:
        print("intersection is ambiguous", t_values)
        return ("ambiguous", [])


def look_at_4d(eye, camera, up, over):

    d = normalize4d(np.subtract(camera, eye))
    a = normalize4d(cross4d(up, over, d))
    b = normalize4d(cross4d(over, d, a))
    c = cross4d(d, a, b)

    return np.array([a, b, c, d])


def transform_view_space(vertices, eye, camera, up, over):
    transform_matrix = look_at_4d(eye, camera, up, over)

    return [np.matmul(transform_matrix, np.subtract(vertex, eye)) for vertex in
            vertices]


def simplex_scence(simplex):
    from math import sin, cos
    from time import sleep
    from mpl_toolkits.mplot3d import Axes3D
    from mpl_toolkits.mplot3d.art3d import Poly3DCollection
    import matplotlib.pyplot as plt

    fig = plt.figure()

    ax = Axes3D(fig)

    min_limits = [min([vert[i] for vert in simplex]) for i in range(3)]
    max_limits = [max([vert[i] for vert in simplex]) for i in range(3)]
    
    ax.set_xlim(min_limits[0] - 1, max_limits[0] + 1)
    ax.set_ylim(min_limits[1] - 1, max_limits[1] + 1)
    ax.set_zlim(min_limits[2] - 1, max_limits[2] + 1)

    plt.ion()
    plt.show() 

    theta_1 = 0
    theta_2 = 0
    theta_3 = 0

    polys = Poly3DCollection([])
    ax.add_collection3d(polys)

    while plt.fignum_exists(fig.number):
        theta_1 += 0.04
        theta_2 += 0.02
        theta_3 += 0.01
        eye = [sin(theta_1) * sin(theta_2) * sin(theta_3),
               sin(theta_1) * sin(theta_2) * cos(theta_3),
               sin(theta_1) * cos(theta_2),
               cos(theta_1)]

        vertices = transform_view_space(simplex, eye, 
                                        [0, 0, 0, 0], [0, 1, 0, 0], [0, 0, 1, 0])
        vertices = slice_xyz_3simplex(vertices)[1]
        vertices = [np.array(vertex).tolist()[:3] for vertex in vertices]

        if len(vertices) > 0:
            polys.set_verts([vertices])
        else:
            polys.set_verts([])

        plt.draw()
        plt.pause(0.000001)

        sleep(0.000001)
