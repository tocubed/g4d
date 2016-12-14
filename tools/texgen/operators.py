import numpy as np
from scipy.interpolate import CubicSpline


def _make_callable(obj):
    if callable(obj):
        return obj
    else:
        return lambda *x: obj


def _make_all_callable(obj_list):
    result = []

    for obj in obj_list:
        result.append(_make_callable(obj))

    return result


def absolute(function):
    return lambda values: np.abs(function(values))


def clamp(function, f_min, f_max):
    f_min, f_max = _make_all_callable((f_min, f_max))

    return lambda values: np.clip(function(values), f_min(values), f_max(values))


def curve(function, control_in, control_out):
    assert control_in.ndim == 1
    assert control_out.shape[0] == control_in.shape[0]

    sort = np.argsort(control_in)
    control_in = control_in[sort]
    control_out = control_out[sort]

    curve = CubicSpline(control_in, control_out)

    return lambda values: curve(function(values))


def power(function, exponent):
    exponent = _make_callable(exponent) 

    return lambda values: np.power(function(values), exponent(values))


def invert(function):
    return lambda values: -function(values)


def scale_bais(function, scale, bias):
    scale, bais = _make_all_callable(scale, bias)

    return lambda values: bias(values) + (scale(values) * function(values))


def add(*functions):
    functions = _make_all_callable(functions)

    return lambda values: np.sum([f(values) for f in functions], axis=0)


def max(*functions):
    functions = _make_all_callable(functions)

    return lambda values: np.amax([f(values) for f in functions], axis=0)


def min(*functions):
    functions = _make_all_callable(functions)

    return lambda values: np.amin([f(values) for f in functions], axis=0)


def multiply(*functions):
    functions = _make_all_callable(functions)

    return lambda values: np.prod([f(values) for f in functions], axis=0)


def mix(a, b, factor):
    a, b, factor = _make_all_callable((a, b, factor))

    def do_mix(values):
        factors = factor(values)
        return factors * a(values) + (1 - factors) * b(values)

    return do_mix


def select(a, b, c, c_min, c_max):
    a, b, c, c_min, c_max = _make_all_callable((a, b, c, c_min, c_max))

    def do_select(values):
        c_values = c(values)
        b_keep = (c_min(values) < c_values) & (c_values < c_max(values))

        result = np.copy(a(values))
        np.copyto(result, b(values), where=keep)

        return result

    return do_select

def compose(a, b):
    return lambda values: a(b(values))
