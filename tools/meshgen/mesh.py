from csg import ConvexPolytope
from scipy.spatial import Delaunay
import struct

class Mesh(object):

    __slots__ = ("vertices", "indices")

    def __init__(self, polytopes=None):
        self.vertices = []
        self.indices = []

        if polytopes:
            self.add_polytopes(polytopes)

    def add_polytopes(self, polytopes):
        for poly in polytopes:
            offset = len(self.vertices)
            for vertex in poly.vertices:
                vertex = vertex.clone()
                vertex.point = poly.plane.local_point_to_global(vertex.point)
                self.vertices.append(vertex)

            delaunay = Delaunay([v.point for v in poly.vertices])
            self.indices.extend(offset + delaunay.simplices.flatten())

    def to_bytes(self):
        vertex_bytes = struct.pack("<I", len(self.vertices))
        for vertex in self.vertices:
            vertex_bytes += vertex.to_bytes()

        index_bytes = struct.pack("<I", len(self.indices))
        for index in self.indices:
            index_bytes += struct.pack("<I", index)

        return vertex_bytes + index_bytes

    def save_to_file(self, name):
        with open(name, 'wb') as f:
            f.write(self.to_bytes())
