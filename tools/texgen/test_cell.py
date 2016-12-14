from cell_noise import cell_noise, CellMethod, DistanceMethod
from preview import preview_2D, preview_3D, preview_2D_RGB, preview_3D_RGB
from operators import compose, multiply, clamp


def test_cell(seed = 1.0, domain_scale = 4):
    cells = cell_noise(CellMethod.second_minus_first, DistanceMethod.euclidean,
                       seed = seed)
    domain = multiply(lambda points: points, domain_scale)

    return clamp(compose(cells, domain), 0.0, 1.0)


def test_cell_rgb(seeds = (1.0, 2.0, 3.0), domain_scales = (4, 4, 4)):
    red = test_cell(seeds[0], domain_scales[0])
    green = test_cell(seeds[1], domain_scales[1])
    blue = test_cell(seeds[2], domain_scales[2])

    return (red, green, blue)


if __name__ == '__main__':

    gray = test_cell()

    preview_2D([256, 256], gray)
    preview_3D([64, 64, 64], gray)

    preview_2D_RGB([256, 256], *test_cell_rgb())
    preview_3D_RGB([64, 64, 64], *test_cell_rgb())
