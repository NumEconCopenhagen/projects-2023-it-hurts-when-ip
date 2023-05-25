import numpy as np
from matplotlib import pyplot as plt
from matplotlib import cm
from scipy import optimize

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
    return 20 * (35 - price) * popularity(performances)

# Function to calculate revenue based on ticket price, performances per year, and number of seats
def revenue(price, performances, seats=np.inf):
    return price * np.minimum(seats, demand(price, performances)) # quantity sold is capped at number of seats

# Function to estimate venue cost coeffecients based on number of seats
def estimate_venue_cost_fn(venues):

    # Function to create venue cost functions with different coefficients
    def create_venue_cost_fn(a, b, c):
        def venue_cost(seats):
            return a * seats**b + c
        return venue_cost
    
    # Function to calculate moment-by-moment difference for some venue cost function
    def moment_diff(venue_cost):
        return [venue['cost'] - venue_cost(venue['seats']) for venue in venues] 
    
    # Function to calculate the weighted error for some venue cost function
    def weighted_error(a, b, c, W=None):
        if W==None: W=np.eye(len(venues))
        venue_cost = create_venue_cost_fn(a, b, c)
        diff = np.array(moment_diff(venue_cost))
        return diff @ W @ diff 
    
    # Objective function to minimize difference between data and venue cost function
    def obj(x):
        return weighted_error(x[0], x[1], x[2])
    
    # Perform minimization
    res = optimize.minimize(obj, (1,1,1), method='Nelder-Mead', bounds=[(0, 50), (0, 2), (-100, 100)], options={'maxfev':1e6})
    print('Difference with data minimized with:\n', f'a = {res.x[0]:5.3f}, b = {res.x[1]:5.3f}, c = {res.x[2]:5.3f}')

    # Overwrite undefined venue cost function
    global venue_cost
    venue_cost = create_venue_cost_fn(res.x[0],res.x[1],res.x[2])

    return venue_cost

# Function to calculate profit when venue size exactly matches demand
def profit(price, performances):
    return revenue(price, performances) - venue_cost(demand(price, performances))

# Function to calculate profit when venue size is fixed
def profit_in_venue(price, performances, seats):
    return revenue(price, performances, seats) - venue_cost(seats)
