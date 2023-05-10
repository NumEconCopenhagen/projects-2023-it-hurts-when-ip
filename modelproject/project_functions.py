import numpy as np
from matplotlib import pyplot as plt
from matplotlib import cm

# Function to plot a 3D graph
def plot3D(func, xs, ys, *args, ax=None):
    if ax == None: ax = plt.figure().add_subplot(projection='3d')
    x_grid, y_grid = np.meshgrid(xs, ys)
    z_grid = func(x_grid, y_grid, *args)
    ax.plot_surface(x_grid, y_grid, z_grid, cmap=cm.jet)
    return ax

# Function to calculate hype score based on performances per year
def hype(performances):
    return 1 - performances * 0.25

# Function to calculate visibility score based on performances per year
def visibility(performances):
    return performances * 0.25

# Function to calculate popularity score based on performances per year
def popularity(performances):
    return hype(performances)**0.5 * visibility(performances)**0.8

# Function to calculate demand based on ticket price and performances per year
def demand(price, performances):
    return 20 * (50 - price) * popularity(performances)

# Function to calculate revenue based on ticket price, performances per year, and number of seats
def revenue(price, performances, seats=np.inf):
    return price * np.minimum(seats, demand(price, performances)) # quantity sold is capped at number of seats

# Function to calculate venue cost based on number of seats
def venue_cost(seats):
    seats = np.maximum(0, seats)
    return 5 * seats ** 0.95

# Function to calculate profit when venue size exactly matches demand
def profit(price, performances):
    return revenue(price, performances) - venue_cost(demand(price, performances))

# Function to calculate profit when venue size is fixed
def profit_in_venue(price, performances, seats):
    return revenue(price, performances, seats) - venue_cost(seats)
