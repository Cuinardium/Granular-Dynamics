import utils
import plots

discharge_times = utils.load_discharges('data/discharges.txt')
obstacles = utils.load_obstacles('data/obstacles.txt')
snapshots = utils.load_snapshots('data/snapshots.txt')
config = utils.load_config('data/config.txt')

plots.plot_cumulative_discharges(discharge_times, 'data/discharges.png')

# Get the first snapshot's particle positions
first_snapshot = snapshots[next(iter(snapshots))]  # Get the first snapshot (the one with the smallest time)

# Plot the initial state
plots.plot_initial_state(config, obstacles, first_snapshot, 'data/initial_state.png')
