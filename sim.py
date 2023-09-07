import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation


def make_TeX_label(tau0, p, q):
    return r'''$\displaystyle{\tau_0 = %s, \quad p = %s, \quad q = %s, \quad f \colon n \mapsto \frac{n(1-p)}{8}+p}$''' % (tau0, p, q)

def f(p, x, tot=8):
    # return np.power(p, 1-x/8)
    return x*(1-p)/tot + p

# Function to update the matrix for each time step
def update(frameNum, plt_axis, img, grid, N, p, q):
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
    plt_axis.set_ylabel(r"\noindent Rate: ${:.2f}$ \\ Step: ${}$".format(rate, frameNum+1), rotation=0, labelpad=50)
    return img

# Constants
N = 200
MAX_ITER = 180
# Initial rate of the system
tau0 = 1e-4
p = 1e-4 # proba of starting if no neighbors are active
q = 0.4 # proba of continuing if no neighbors are active

# time step in milliseconds
updateInterval = 50

# Create a random initial grid
grid = np.random.choice([0, 1], N*N, p=[1-tau0, tau0]).reshape(N, N)
# img = plt.imshow(grid, interpolation='nearest', cmap='binary')

plt.rcParams.update({"text.usetex": True, "font.family": "serif"})

# Create the figure and axis for the animationb
fig, ax = plt.subplots()
ax.set_xticks([])
ax.set_yticks([])
ax.set_title(r'Simulation with 1\textsuperscript{st} order neighbourhood')
ax.set_xlabel(make_TeX_label(tau0, p, q))
ax.set_ylabel(r'\noindent Rate: ${:.2f}$ \\ Step: $0$'.format(tau0), rotation=0, labelpad=50)

img = ax.imshow(grid, interpolation='none', cmap='binary')


ani = animation.FuncAnimation(fig, update, fargs=(ax, img, grid, N, p, q), interval=updateInterval, save_count=MAX_ITER, repeat=False)
ani.save('sim.mp4', extra_args=['-vcodec', 'libx264'], progress_callback=lambda i, n: print(f'Rendering ({round(100*i/n,2)}%)\r', end=''), dpi=300)

plt.show()
