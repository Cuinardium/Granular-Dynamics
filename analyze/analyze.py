import utils
import plots

output_directory = 'data/analysis'
plot_directory = 'data/plots'

discharge_times = utils.load_discharges(f'{output_directory}/discharges.txt')
obstacles = utils.load_obstacles(f'{output_directory}/obstacles.txt')
snapshots = utils.load_snapshots(f'{output_directory}/snapshots.txt')
config = utils.load_config(f'{output_directory}/config.txt')


# Get the first snapshot's particle positions
first_snapshot = snapshots[next(iter(snapshots))]  # Get the first snapshot (the one with the smallest time)

# Plot the initial state
plots.plot_initial_state(config, obstacles, first_snapshot, f'{plot_directory}/initial_state.png')


def equivalent_simulations():
    # Set parameters and execute the simulation
    W = 20
    L = 70
    M = 100
    N = 100
    R = 1
    r = 1
    m = 1
    A = 1
    k_n = 250
    k_t = 500
    dt = 0.01
    dt2 = 0.01
    tf = 10

    discharge_times = []
    for i in range(5):
        # Execute the simulation
        utils.execute_granular_dynamics_jar(
            W, L, M, N, R, r, m, A, k_n, k_t, dt, dt2, tf, output_directory
        )

        # Load the discharge times
        discharge_times.append(utils.load_discharges(f'{output_directory}/discharges.txt'))

    # Plot the cumulative discharges in one graph
    plots.plot_cumulative_discharges(discharge_times, f'{plot_directory}/equivalent_simulations.png')


equivalent_simulations()