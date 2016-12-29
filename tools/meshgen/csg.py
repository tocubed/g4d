import itertools
import numpy as np
from scipy.spatial import ConvexHull
import struct
import random


class Vertex(object):

    __slots__ = ("point")

    def __init__(self, point):
        self.point = point

    def interpolate(self, other, t):
        point = np.multiply(self.point, t) + np.multiply(other.point, 1 - t)
        return Vertex(point)

    def flip(self):
        pass

    def clone(self):
        return Vertex(np.copy(self.point))

    def to_bytes(self):
        return self.point.astype("<f4").tobytes()

    @property
    def dimension(self):
        return self.point.size


class ConvexPolytope(object):

    __slots__ = ("vertices", "hull", "plane", "attributes")

    def __init__(self, vertices, plane, attributes={}):
        self.vertices = vertices
        self.hull = ConvexHull([v.point for v in vertices])
        self.plane = plane
        self.attributes = attributes

    def vertex_indices(self):
        return self.hull.vertices

    def edge_indices(self):
        simplex_edges = list(itertools.combinations(range(self.dimension), 2))
        edges = set()
        for simplex in self.hull.simplices:
            edges |= {frozenset((simplex[i], simplex[j])) for i, j in simplex_edges}
        return edges

    def flip(self):
        self.plane.flip()
        for v in self.vertices:
            v.flip()

    def clone(self):
        vertices = [v.clone() for v in self.vertices]
        return ConvexPolytope(vertices, self.plane.clone(), self.attributes)

    @property
    def points(self):
        return self.hull.points

    @property
    def volume(self):
        return self.hull.volume

    @property
    def area(self):
        return self.hull.area

    @property
    def dimension(self):
        return self.vertices[0].dimension


class Plane(object):

    __slots__ = ("normal", "distance")

    EPSILON = 1.0e-10

    def __init__(self, normal, distance=0.0):
        self.normal = normal
        self.distance = distance

    def split_polytope(self, polytope):
        COPLANAR = 0
        FRONT = 1
        BACK = 2
        SPANNING = FRONT | BACK

        plane = polytope.plane.global_plane_to_local(self)

        vertices = polytope.vertices
        indices = polytope.vertex_indices()
        distances = plane.distance_to_point(polytope.points[indices])

        types = {}
        polytope_type = COPLANAR
        for index, distance in zip(indices, distances):
            v_type = FRONT if distance > Plane.EPSILON else \
                     BACK if distance < -Plane.EPSILON else COPLANAR
            types[index] = v_type
            polytope_type |= v_type
        
        if polytope_type == COPLANAR:
            if np.dot(self.normal, polytope.plane.normal) > 0:
                return (None, None, polytope, None)
            else:
                return (None, None, None, polytope)
        elif polytope_type == FRONT:
            return (polytope, None, None, None)
        elif polytope_type == BACK:
            return (None, polytope, None, None)
        else:
            front = []
            back = []
            for index, v_type in types.items():
                if v_type == FRONT:
                    front.append(vertices[index])
                elif v_type == BACK:
                    back.append(vertices[index])
                else:
                    front.append(vertices[index])
                    back.append(vertices[index].clone())

            for i, j in polytope.edge_indices():
                if types[i] | types[j] == SPANNING:
                    t = plane.intersect_edge(polytope.points[i], polytope.points[j])
                    v = vertices[i].interpolate(vertices[j], t)
                    front.append(v)
                    back.append(v.clone())

            front_polytope = ConvexPolytope(front, polytope.plane.clone()
                                            , polytope.attributes)
            back_polytope = ConvexPolytope(back, polytope.plane.clone()
                                           , polytope.attributes)

            return (front_polytope, back_polytope, None, None)

    def global_plane_to_local(self, p):
        half_vector = np.copy(self.normal)
        half_vector[-1] += 1

        half_vector_norm = np.linalg.norm(half_vector)
        if half_vector_norm < Plane.EPSILON:
            half_vector[:] = 0
        else:
            half_vector /= half_vector_norm

        reflected = p.normal - 2 * self.normal * np.dot(self.normal, p.normal)
        normal = reflected - 2 * half_vector * np.dot(half_vector, reflected)
        normal = normal[:-1]

        diff_vector = p.distance * p.normal - self.distance * self.normal
        distance = np.dot(p.normal, diff_vector)

        normal_norm = np.linalg.norm(normal)
        if normal_norm < Plane.EPSILON:
            normal[:] = 0
        else:
            normal /= normal_norm
            distance /= normal_norm

        return Plane(normal, distance)

    def local_point_to_global(self, p):
        p = np.insert(p, np.shape(p)[-1], 0, axis=-1)

        half_vector = np.copy(self.normal)
        half_vector[-1] += 1

        half_vector_norm = np.linalg.norm(half_vector)
        if half_vector_norm < Plane.EPSILON:
            half_vector[:] = 0
        else:
            half_vector /= half_vector_norm

        rotated = p - 2 * half_vector * np.dot(p, half_vector)
        return rotated + self.distance * self.normal

    def global_point_to_local(self, p):
        half_vector = np.copy(self.normal)
        half_vector[-1] += 1

        half_vector_norm = np.linalg.norm(half_vector)
        if half_vector_norm < Plane.EPSILON:
            half_vector[:] = 0
        else:
            half_vector /= half_vector_norm

        translated = p - self.distance * self.normal
        rotated = translated - 2 * half_vector * np.dot(translated, half_vector)

        return rotated[... , :-1]

    def intersect_edge(self, p1, p2):
        d1 = np.dot(p1, self.normal) 
        d2 = np.dot(p2, self.normal)

        d = d2 - d1
        if d == 0:
            return 0.5
        else:
            return (d2 - self.distance) / d

    def distance_to_point(self, p):
        return np.dot(p, self.normal) - self.distance

    def flip(self):
        self.normal = -self.normal
        self.distance = -self.distance

    def clone(self):
        return Plane(np.copy(self.normal), self.distance)

    @property
    def origin(self):
        return self.normal * self.distance

    @property
    def dimension(self):
        return self.normal.size


class BSP(object):

    __slots__ = ("plane", "front", "back", "polytopes")

    def __init__(self, polytopes=None):
        self.plane = None
        self.front = None
        self.back = None
        self.polytopes = []
        if polytopes:
            self.build(polytopes)

    def build(self, polytopes):
        if not polytopes:
            return

        if not self.plane:
            self.plane = polytopes[0].plane.clone()

        front = []
        back = []
        for poly in polytopes:
            f, b, cf, cb = self.plane.split_polytope(poly)
            if f: front.append(f)
            if b: back.append(b)
            if cf: self.polytopes.append(cf)
            if cb: self.polytopes.append(cb)

        if front:
            if not self.front:
                self.front = BSP()
            self.front.build(front)
        if back:
            if not self.back:
                self.back = BSP()
            self.back.build(back)

    def clip_to(self, bsp):
        self.polytopes = bsp.clip_polytopes(self.polytopes)
        if self.front:
            self.front.clip_to(bsp)
        if self.back:
            self.back.clip_to(bsp)

    def clip_polytopes(self, polytopes):
        if not self.plane:
            return list(polytopes)

        front = []
        back = []
        for poly in polytopes:
            f, b, cf, cb = self.plane.split_polytope(poly)
            if f: front.append(f)
            if cf: front.append(cf)
            if b: back.append(b)
            if cb: back.append(cb)

        if self.front:
            front = self.front.clip_polytopes(front)
        if self.back:
            back = self.back.clip_polytopes(back)
        else:
            back = []

        return front + back

    def all_polytopes(self):
        polytopes = list(self.polytopes)
        if self.front:
            polytopes += self.front.all_polytopes()
        if self.back:
            polytopes += self.back.all_polytopes()
        return polytopes

    def invert(self):
        self.plane.flip()
        for poly in self.polytopes:
            poly.flip()

        if self.front:
            self.front.invert()
        if self.back: 
            self.back.invert()
        self.front, self.back = self.back, self.front

    def clone(self):
        bsp = BSP()
        bsp.plane = self.plane and self.plane.clone()
        bsp.front = self.front and self.front.clone()
        bsp.back = self.back and self.back.clone()
        bsp.polytopes = [p.clone() for p in self.polytopes]
        return bsp


class CSG(object):

    __slots__ = ("polytopes")

    def __init__(self, polytopes):
        self.polytopes = polytopes

    def union(self, other):
        a = BSP(self.clone().polytopes)
        b = BSP(other.clone().polytopes)
        a.clip_to(b)
        b.clip_to(a)
        b.invert()
        b.clip_to(a)
        b.invert()
        a.build(b.all_polytopes())
        return CSG(a.all_polytopes())

    def subtract(self, other):
        a = BSP(self.clone().polytopes)
        b = BSP(other.clone().polytopes)
        a.invert()
        a.clip_to(b)
        b.clip_to(a)
        b.invert()
        b.clip_to(a)
        b.invert()
        a.build(b.all_polytopes())
        a.invert()
        return CSG(a.all_polytopes())

    def intersect(self, other):
        a = BSP(self.clone().polytopes)
        b = BSP(other.clone().polytopes)
        a.invert()
        b.clip_to(a)
        b.invert()
        a.clip_to(b)
        b.clip_to(a)
        a.build(b.all_polytopes())
        a.invert()
        return CSG(a.all_polytopes())

    def inverse(self):
        csg = self.clone()
        for poly in csg.polytopes:
            poly.flip()
        return csg

    def translate(self, vector):
        csg = self.clone()
        for poly in csg.polytopes:
            parallel = np.dot(poly.plane.normal, vector) #TODO ADD PROPS TO POLYTP
            poly.plane.distance -= parallel

            perp = -np.subtract(vector, poly.plane.normal * parallel)
            translation = poly.plane.global_point_to_local(perp + poly.plane.origin)

            for vertex in poly.vertices:
                vertex.point += translation
        return csg

    def scale(self, factors):
        pass

    def clone(self): # TODO USE BETTER HEURISTICS, AND DONT USE THEM HERE IN CLONE
        polys = [p.clone() for p in self.polytopes]
        random.shuffle(polys)
        return CSG(polys)
        #return CSG([p.clone() for p in self.polytopes])
