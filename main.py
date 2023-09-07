
import matplotlib.pyplot as plt
import matplotlib.animation as animation
import sys, getopt
from sim import *

if __name__ == '__main__':
    # Constants
    N = 100
    MAX_ITER = 10
    # Initial rate of the system
    tau0 = 1e-4
    p = 1e-4 # proba of starting if no neighbors are active
    q = 0.4 # proba of continuing if no neighbors are active

    # time step in milliseconds
    updateInterval = 50

    texified = False
    saved = False
    # getopt
    try:
        opts, args = getopt.getopt(sys.argv[1:], "hsn:N:o:t:p:q:", ["help", "save", "ngrid=", "MAXITER=", "output=", "t0=", "p=", "q="])
    except getopt.GetoptError as err:
        print(err)
        sys.exit(2)
    for opt, arg in opts:
        if opt in ("-h", "--help"):
            print(
                """Usage: python main.py -s 1 -n <N> -I <MAXITER> -o <TeX output> -p <p> -q <q>\n
                or: python sim.py --save 1 --ngrid=<N> --MAXITER=<MAXITER> --output=<TeX output> --p=<p> --q=<q>\n
                Options:
                    * -h, --help: display this help and exit
                    * -s, --save: save the animation as a mp4 file
                    * -n, --ngrid: size of the grid (default: 100)
                    * -I, --MAXITER: number of iterations (default: 10)
                    * -o, --output: TeX output (default: 0)
                    * -t, --t0: initial rate of the system (default: 1e-4)
                    * -p, --p: probability of starting if no neighbors are active (default: 1e-4)
                    * -q, --q: probability of continuing if no neighbors are active (default: 0.4)
                """
            )
            sys.exit()
        elif opt in ("-n", "--ngrid"):
            N = int(arg)
        elif opt in ("-I", "--MAXITER"):
            MAX_ITER = int(arg)
        elif opt in ("-o", "--output"):
            plt.rcParams.update({"text.usetex": True, "font.family": "serif"})
            texified = bool(int(arg))
        elif opt in ("-t", "--t0"):
            tau0 = float(arg)
        elif opt in ("-p", "--p"):
            p = float(arg)
        elif opt in ("-q", "--q"):
            q = float(arg)
        elif opt in ("-s", "--save"):
            saved = True
    
    plt.rcParams['font.size'] = 8

    # Create a random initial grid
    grid = np.random.choice([0, 1], N*N, p=[1-tau0, tau0]).reshape(N, N)

    # Create the figure and axis for the animationb
    fig, ax = plt.subplots()
    ax.set_xticks([])
    ax.set_yticks([])
    ax.set_title(make_title(texified))
    ax.set_xlabel(make_xlabel(texified, tau0, p, q))
    ax.set_ylabel(make_ylabel(texified, tau0, 0), rotation=0, labelpad=50)

    img = ax.imshow(grid, interpolation='none', cmap='viridis')

    ani = animation.FuncAnimation(fig, update, fargs=(texified, ax, img, grid, N, p, q), interval=updateInterval, save_count=MAX_ITER, repeat=False)
    if saved:
        ani.save('sim.mp4', extra_args=['-vcodec', 'libx264'], progress_callback=lambda i, n: print(f'Rendering ({round(100*i/n,2)}%)\r', end=''), dpi=300)
    else:
        plt.show()