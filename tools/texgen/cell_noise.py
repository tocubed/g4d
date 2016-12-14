from enum import Enum
import numpy as np


def _cell_noise_1_values(point_func, distance_func, distance_final_func,
                         value_func):

    def values(points):
        offsets, cells = np.modf(points)

        closest = np.full(points.shape[1:], np.inf)

        for neighbor in np.ndindex((3,) * points.shape[0]):
            neighbor = np.array(neighbor, ndmin=points.ndim).T - 1
            deltas = neighbor - offsets + point_func(cells + neighbor) 

            distances = distance_func(deltas)
            closest = np.fmin(closest, distances)

        closest = distance_final_func(closest)

        return value_func(closest)

    return values


def _cell_noise_2_values(point_func, distance_func, distance_final_func,
                         value_func):

    def values(points):
        offsets, cells = np.modf(points)

        closest_1 = np.full(points.shape[1:], np.inf)
        closest_2 = np.full(points.shape[1:], np.inf)

        for neighbor in np.ndindex((3,) * points.shape[0]):
            neighbor = np.array(neighbor, ndmin=points.ndim).T - 1
            deltas = neighbor - offsets + point_func(cells + neighbor) 

            distances = distance_func(deltas)

            lt_closest_1 = distances < closest_1
            lt_closest_2 = ~lt_closest_1 & (distances < closest_2)

            np.copyto(closest_2, closest_1, where=lt_closest_1)
            np.copyto(closest_1, distances, where=lt_closest_1)
            np.copyto(closest_2, distances, where=lt_closest_2)

        closest_1 = distance_final_func(closest_1)
        closest_2 = distance_final_func(closest_2)

        return value_func(closest_1, closest_2)

    return values


def _cell_noise_3_values(point_func, distance_func, distance_final_func,
                         value_func):

    def values(points):
        offsets, cells = np.modf(points)

        closest_1 = np.full(points.shape[1:], np.inf)
        closest_2 = np.full(points.shape[1:], np.inf)
        closest_3 = np.full(points.shape[1:], np.inf)

        for neighbor in np.ndindex((3,) * points.shape[0]):
            neighbor = np.array(neighbor, ndmin=points.ndim).T - 1
            deltas = neighbor - offsets + point_func(cells + neighbor) 

            distances = distance_func(deltas)

            lt_closest_1 = distances < closest_1
            lt_closest_2 = ~lt_closest_1 & (distances < closest_2)
            lt_closest_3 = ~lt_closest_1 & ~lt_closest_2 & (distances < closest_3)

            np.copyto(closest_3, closest_2, where=lt_closest_1)
            np.copyto(closest_2, closest_1, where=lt_closest_1)
            np.copyto(closest_1, distances, where=lt_closest_1)
            np.copyto(closest_3, closest_2, where=lt_closest_2)
            np.copyto(closest_2, distances, where=lt_closest_2)
            np.copyto(closest_3, distances, where=lt_closest_3)

        closest_1 = distance_final_func(closest_1)
        closest_2 = distance_final_func(closest_2)
        closest_3 = distance_final_func(closest_3)

        return value_func(closest_1, closest_2, closest_3)

    return values


_almost_primes = np.array([12.9898, 78.233, 127.1, 311.7, 269.5, 183.3, 149.13, 
                           619.9, 23.1345, 61.254, 373.7, 283.4, 11.6523, 71.8,
                           438.1, 100.23])


def _fract_sin_dot_prime(seed):

    def values(points):
        coords = seed * points
        vectors = np.empty_like(coords)

        for i in range(coords.shape[0]):
            prime_begin = i * coords.shape[0]
            prime_end = (i + 1) * coords.shape[0]
            prime_vector = _almost_primes[prime_begin:prime_end] 

            vectors[i] = np.tensordot(coords, prime_vector, axes=(0, 0))

        return (np.sin(vectors) * 43758.5453) % 1.0

    return values


class CellMethod(Enum):

    first  = (_cell_noise_1_values, lambda  x: x)
    second = (_cell_noise_2_values, lambda *x: x[1])
    third  = (_cell_noise_3_values, lambda *x: x[2])

    second_minus_first = (_cell_noise_2_values, lambda *x: x[1] - x[0])
    third_minus_second = (_cell_noise_3_values, lambda *x: x[2] - x[1])
    third_minus_first  = (_cell_noise_3_values, lambda *x: x[2] - x[0])

    def __init__(self, noise_func, value_func):
        self.noise_func = noise_func
        self.value_func = value_func


class DistanceMethod(Enum):

    euclidean = (lambda x: np.sum(x * x, axis=0), lambda x: np.sqrt(x))
    manhattan = (lambda x: np.sum(np.abs(x), axis=0), lambda x: x)
    chebyshev = (lambda x: np.amax(np.abs(x), axis=0), lambda x: x)
    minkowski3 = (lambda x: np.sum(np.abs(x * x * x), axis=0), lambda x: np.cbrt(x))
    euclidean_squared = (lambda x: np.sum(x * x, axis=0), lambda x: x)

    def __init__(self, distance_func, distance_final_func):
        self.distance_func = distance_func
        self.distance_final_func = distance_final_func


def cell_noise(cell_method = CellMethod.first, 
               distance_method = DistanceMethod.euclidean,
               seed = 1.0):

    point_func = _fract_sin_dot_prime(seed)

    noise_func = cell_method.noise_func
    value_func = cell_method.value_func

    distance_func = distance_method.distance_func
    distance_final_func = distance_method.distance_final_func

    return noise_func(point_func, distance_func, distance_final_func, value_func)
