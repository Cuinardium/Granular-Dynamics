import matplotlib.pyplot as plt
import numpy as np

def plot_cumulative_discharges(discharge_times, file_path="discharges.png"):
    discharge_times = sorted(discharge_times)
    
    # Generate cumulative discharge count
    cumulative_discharges = np.arange(1, len(discharge_times) + 1)

    # Plot cumulative discharges over time
    plt.figure(figsize=(10, 6))
    plt.plot(discharge_times, cumulative_discharges, marker='o', linestyle='-')
    plt.xlabel('Tiempo (s)')
    plt.ylabel('Descargas')

    plt.grid(True)

    plt.savefig(file_path)
    plt.close()


def plot_initial_state(config, obstacles, first_snapshot, file_path="initial_state.png"):
    plt.figure(figsize=(10, 10))
    plt.xlim(0, config['length'])
    plt.ylim(0, config['width'])
    
    # Plot obstacles
    for (x, y) in obstacles:
        circle = plt.Circle((x, y), config['obstacle_radius'], color='red', alpha=0.5, label='Obstacle' if 'Obstacle' not in plt.gca().get_legend_handles_labels()[1] else "")
        plt.gca().add_artist(circle)

    # Plot particles from the first snapshot
    particle_xs, particle_ys = zip(*first_snapshot)
    for (x, y) in zip(particle_xs, particle_ys):
        circle = plt.Circle((x, y), config['particle_radius'], color='blue', alpha=0.7, label='Particle' if 'Particle' not in plt.gca().get_legend_handles_labels()[1] else "")
        plt.gca().add_artist(circle)
    
    plt.gca().set_aspect('equal', adjustable='box')
    plt.legend()
    plt.grid()

    plt.savefig(file_path)
