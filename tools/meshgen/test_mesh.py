from csg import *
from mesh import Mesh
import brushes
import numpy as np


class VertexTextured(object):

    __slots__ = ("point", "tex_coord")

    def __init__(self, point, tex_coord):
        self.point = point
        self.tex_coord = tex_coord

    def interpolate(self, other, t):
        point = np.multiply(self.point, t) + np.multiply(other.point, 1 - t)
        tex_coord = np.multiply(self.tex_coord, t) + np.multiply(other.tex_coord, 1 - t)
        return VertexTextured(point, tex_coord)

    def flip(self):
        pass

    def clone(self):
        return VertexTextured(np.copy(self.point), np.copy(self.tex_coord))

    def to_bytes(self):
        point = self.point.astype("<f4").tobytes()
        tex_coord = self.tex_coord.astype("<f4").tobytes()
        return point + tex_coord

    @property
    def dimension(self):
        return self.point.size


def hypercube():
    hc = brushes.hypercube()

    polys = []
    for poly in hc.polytopes:
        # Use vertex point as tex_coord
        vertices = [VertexTextured(v.point, v.point) for v in poly.vertices]
        polys.append(ConvexPolytope(vertices, poly.plane))

    return CSG(polys)


if __name__ == '__main__':
    brush = hypercube()

    for i in range(4):
        translation = np.random.normal(size=4)
        brush = brush.union(brush.translate(translation))
        print("building brush with polys: ", len(brush.polytopes))

    print("saving mesh to file...")
    Mesh(brush.polytopes).save_to_file("germa.m4d")
