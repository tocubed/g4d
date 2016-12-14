import matplotlib.pyplot as plt
import matplotlib.animation as anim
import numpy as np


def preview_2D(dimensions, gray):

    x = np.linspace(0, 1, dimensions[0])
    y = np.linspace(0, 1, dimensions[1])
    xy = np.array(np.meshgrid(x, y))

    grays = gray(xy)

    plt.imshow(grays, vmin=0.0, vmax=1.0, cmap='gray')
    plt.show()


def preview_3D(dimensions, gray):

    x = np.linspace(0, 1, dimensions[0])
    y = np.linspace(0, 1, dimensions[1])
    z = np.linspace(0, 1, dimensions[2])
    xyz = np.array(np.meshgrid(x, y, z))

    grays = gray(xyz)
    
    fig = plt.figure()

    images = []
    for z_i in range(dimensions[2]):
        image = plt.imshow(grays[:, :, z_i], vmin=0.0, vmax=1.0, 
                           cmap='gray', animated=True)
        images.append([image])

    animation = anim.ArtistAnimation(fig, images, interval=20, blit=True)

    plt.show()


def preview_2D_RGB(dimensions, red, green, blue):

    x = np.linspace(0, 1, dimensions[0])
    y = np.linspace(0, 1, dimensions[1])
    xy = np.array(np.meshgrid(x, y))

    reds = red(xy)
    greens = green(xy)
    blues = blue(xy)

    rgbs = np.stack([reds, greens, blues], axis=-1)

    plt.imshow(rgbs, vmin=0.0, vmax=1.0)
    plt.show()


def preview_3D_RGB(dimensions, red, green, blue):

    x = np.linspace(0, 1, dimensions[0])
    y = np.linspace(0, 1, dimensions[1])
    z = np.linspace(0, 1, dimensions[2])
    xyz = np.array(np.meshgrid(x, y, z))

    reds = red(xyz)
    greens = green(xyz)
    blues = blue(xyz)

    rgbs = np.stack([reds, greens, blues], axis=-1)
    
    fig = plt.figure()

    images = []
    for z_i in range(dimensions[2]):
        image = plt.imshow(rgbs[:, :, z_i], vmin=0.0, vmax=1.0, animated=True)
        images.append([image])

    animation = anim.ArtistAnimation(fig, images, interval=20, blit=True)

    plt.show()
