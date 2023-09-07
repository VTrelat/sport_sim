from aux import *
import numpy as np

def f(p, x, tot=8):
    # return np.power(p, 1-x/8)
    return x*(1-p)/tot + p

# Function to update the matrix for each time step
def update(frameNum, texified, plt_axis, img, grid, N, p, q):
    newGrid = grid.copy()
    rate=0
    for i in range(N):
        for j in range(N):
            # Compute the sum of the eight neighbors
            total1 = (grid[i, (j-1)%N] + grid[i, (j+1)%N] +
                    grid[(i-1)%N, j] + grid[(i+1)%N, j] +
                    grid[(i-1)%N, (j-1)%N] + grid[(i-1)%N, (j+1)%N] +
                    grid[(i+1)%N, (j-1)%N] + grid[(i+1)%N, (j+1)%N])
            # total2 = (grid[(i-2)%N, (j-2)%N] + grid[(i-2)%N, (j-1)%N] + grid[(i-2)%N, j] + grid[(i-2)%N, (j+1)%N] + grid[(i-2)%N, (j+2)%N] +
            #         grid[(i-1)%N, (j-2)%N] + grid[(i-1)%N, (j+2)%N] +
            #         grid[i, (j-2)%N] + grid[i, (j+2)%N] +
            #         grid[(i+1)%N, (j-2)%N] + grid[(i+1)%N, (j+2)%N] +
            #         grid[(i+2)%N, (j-2)%N] + grid[(i+2)%N, (j-1)%N] + grid[(i+2)%N, j] + grid[(i+2)%N, (j+1)%N] + grid[(i+2)%N, (j+2)%N])

# i-2, j-2 | i-2, j-1 | i-2, j | i-2, j+1 | i-2, j+2
# _________|__________|________|__________|_________
# i-1, j-2 | i-1, j-1 | i-1, j | i-1, j+1 | i-1, j+2
# _________|__________|________|__________|_________
# i, j-2   | i, j-1   | i, j   | i, j+1   | i, j+2
# _________|__________|________|__________|_________
# i+1, j-2 | i+1, j-1 | i+1, j | i+1, j+1 | i+1, j+2
# _________|__________|________|__________|_________
# i+2, j-2 | i+2, j-1 | i+2, j | i+2, j+1 | i+2, j+2
# _________|__________|________|__________|_________


            if grid[i, j] == 1:
                # Probability of continuing
                newGrid[i, j] = int(np.random.binomial(1, f(q, total1, 9), 1))
            else:
                # Probability of starting
                newGrid[i, j] = int(np.random.binomial(1, f(p, total1, 9), 1))
            rate += newGrid[i, j]

    rate /= (N*N)
    # Update the data
    img.set_data(newGrid)
    grid[:] = newGrid[:]
    # Update the label
    plt_axis.set_ylabel(make_ylabel(texified, rate, frameNum), rotation=0, labelpad=50)
    return img