import numpy as np
from PIL import Image


def output_2D(dimensions, gray, fp, format='PNG'):

    x = np.linspace(0, 1, dimensions[0])
    y = np.linspace(0, 1, dimensions[1])
    xy = np.array(np.meshgrid(x, y))

    grays = gray(xy)
    grayscale = (255.0 / grays.max() * (grays - grays.min())).astype(np.uint8)

    im = Image.fromarray(grayscale, mode='L')
    im.save(fp, format)


def output_3D(dimensions, gray, fp, format='PNG'):

    x = np.linspace(0, 1, dimensions[0])
    y = np.linspace(0, 1, dimensions[1])
    z = np.linspace(0, 1, dimensions[2])
    xyz = np.array(np.meshgrid(x, y, z))

    grays = gray(xyz)
    grays = grays.reshape((dimensions[0], dimensions[1] * dimensions[2]))

    grayscale = (255.0 / grays.max() * (grays - grays.min())).astype(np.uint8)

    im = Image.fromarray(grayscale, mode='L')
    im.save(fp, format)


def output_2D_RGB(dimensions, red, green, blue, fp, format='PNG'):

    x = np.linspace(0, 1, dimensions[0])
    y = np.linspace(0, 1, dimensions[1])
    xy = np.array(np.meshgrid(x, y))

    reds = red(xy)
    greens = green(xy)
    blues = blue(xy)

    redscale = (255.0 / reds.max() * (reds - reds.min())).astype(np.uint8)
    greenscale = (255.0 / greens.max() * (greens - greens.min())).astype(np.uint8)
    bluescale = (255.0 / blues.max() * (blues - blues.min())).astype(np.uint8)

    rgbscale = np.stack([redscale, greenscale, bluescale], axis=-1)

    im = Image.fromarray(rgbscale, mode='RGB')
    im.save(fp, format)


def output_3D_RGB(dimensions, red, green, blue, fp, format='PNG'):

    x = np.linspace(0, 1, dimensions[0])
    y = np.linspace(0, 1, dimensions[1])
    z = np.linspace(0, 1, dimensions[2])
    xyz = np.array(np.meshgrid(x, y, z))

    reds = red(xyz)
    greens = green(xyz)
    blues = blue(xyz)

    reds = reds.reshape((dimensions[0], dimensions[1] * dimensions[2]))
    greens = greens.reshape((dimensions[0], dimensions[1] * dimensions[2]))
    blues = blues.reshape((dimensions[0], dimensions[1] * dimensions[2]))

    redscale = (255.0 / reds.max() * (reds - reds.min())).astype(np.uint8)
    greenscale = (255.0 / greens.max() * (greens - greens.min())).astype(np.uint8)
    bluescale = (255.0 / blues.max() * (blues - blues.min())).astype(np.uint8)

    rgbscale = np.stack([redscale, greenscale, bluescale], axis=-1)
    
    im = Image.fromarray(rgbscale, mode='RGB')
    im.save(fp, format)
