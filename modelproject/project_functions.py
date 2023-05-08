import numpy as np
from matplotlib import pyplot as plt
from matplotlib import cm


def plot3D(func, xs, ys, *args, ax=None):
    if ax == None: ax = plt.figure().add_subplot(projection='3d')
    x_grid, y_grid = np.meshgrid(xs, ys)
    z_grid = func(x_grid, y_grid, *args)
    ax.plot_surface(x_grid, y_grid, z_grid, cmap=cm.jet)
    return ax