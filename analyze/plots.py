import matplotlib.pyplot as plt
import matplotlib.animation as animation
import numpy as np


def plot_X_vs_Y(Y_values, mean_X, std_X, file_path, X_label, Y_label):
    plt.figure(figsize=(10, 6))
    plt.errorbar(Y_values, mean_X, yerr=std_X, fmt="-o", capsize=5)

    plt.xlabel(X_label)
    plt.ylabel(Y_label)

    plt.grid(True)
    plt.savefig(file_path)
    plt.close()


def plot_cumulative_discharges(discharge_times_list, file_path="discharges.png"):
    plt.figure(figsize=(10, 6))

    for discharge_times in discharge_times_list:
        discharge_times = sorted(discharge_times)

        # Generate cumulative discharge count
        cumulative_discharges = np.arange(1, len(discharge_times) + 1)

        # Plot cumulative discharges over time
        plt.plot(discharge_times, cumulative_discharges, linestyle="-")

    plt.xlabel("Tiempo (s)")
    plt.ylabel("Descargas")

    plt.grid(True)
    plt.savefig(file_path)
    plt.close()


def plot_initial_state(
    config, obstacles, first_snapshot, file_path="initial_state.png"
):
    plt.figure(figsize=(10, 10))
    plt.xlim(0, config["length"])
    plt.ylim(0, config["width"])

    # Plot obstacles
    for x, y in obstacles:
        circle = plt.Circle(
            (x, y),
            config["obstacle_radius"],
            color="red",
            alpha=0.5,
            label=(
                "Obstacle"
                if "Obstacle" not in plt.gca().get_legend_handles_labels()[1]
                else ""
            ),
        )
        plt.gca().add_artist(circle)

    # Plot particles from the first snapshot
    particle_xs, particle_ys = zip(*first_snapshot)
    for x, y in zip(particle_xs, particle_ys):
        circle = plt.Circle(
            (x, y),
            config["particle_radius"],
            color="blue",
            alpha=0.7,
            label=(
                "Particle"
                if "Particle" not in plt.gca().get_legend_handles_labels()[1]
                else ""
            ),
        )
        plt.gca().add_artist(circle)

    plt.gca().set_aspect("equal", adjustable="box")

    plt.savefig(file_path)


# Mean and st flow rates are a dict of obtacle_count -> dict of acceleration -> mean/stdev
# I need to plot for each obstacle count the mean and stdev of the flow rate for each acceleration
# So i should have a curve for each obstacle_count of acceleration vs flow_rate
# Put the obstacl counts as legend
def plot_flow_rate_vs_acceleration(
    mean_flow_rates,
    std_flow_rates,
    output_file,
):

    plt.figure(figsize=(10, 6))

    for obstacle_count, mean_flow_rate in mean_flow_rates.items():
        std_flow_rate = std_flow_rates[obstacle_count]

        accelerations = list(mean_flow_rate.keys())
        mean_flow_rate = list(mean_flow_rate.values())
        std_flow_rate = list(std_flow_rate.values())

        # Sort the data by acceleration
        accelerations, mean_flow_rate, std_flow_rate = zip(
            *sorted(zip(accelerations, mean_flow_rate, std_flow_rate))
        )

        plt.errorbar(
            accelerations,
            mean_flow_rate,
            yerr=std_flow_rate,
            fmt="-o",
            capsize=5,
            label=f"{obstacle_count} obstaculos",
        )

    plt.xlabel("Aceleración (cm/s^2)")
    plt.ylabel("Caudal (partículas/s)")

    plt.legend()
    plt.grid(True)
    plt.savefig(output_file)
    plt.close()


# Mean and st flow rates are a dict of acceleration -> dict of obstacle count -> mean/stdev
# I need to plot for each acceleration the mean and stdev of the flow rate for each obstacle count
# So i should have a curve for each acceleration of obstacle count vs flow_rate
# Put the acceleration as legend
def plot_flow_rate_vs_obstacle_count(
    mean_flow_rates,
    std_flow_rates,
    output_file,
):

    plt.figure(figsize=(10, 6))

    for acceleration, mean_flow_rate in mean_flow_rates.items():
        std_flow_rate = std_flow_rates[acceleration]

        obstacle_counts = list(mean_flow_rate.keys())
        mean_flow_rate = list(mean_flow_rate.values())
        std_flow_rate = list(std_flow_rate.values())

        # Sort the data by obstacle count
        obstacle_counts, mean_flow_rate, std_flow_rate = zip(
            *sorted(zip(obstacle_counts, mean_flow_rate, std_flow_rate))
        )

        plt.errorbar(
            obstacle_counts,
            mean_flow_rate,
            yerr=std_flow_rate,
            fmt="-o",
            capsize=5,
            label=f"{acceleration} cm/s^2",
        )

    plt.xlabel("Cantidad de obstáculos")
    plt.ylabel("Caudal (partículas/s)")

    plt.legend()
    plt.grid(True)
    plt.savefig(output_file)
    plt.close()


def plot_resistence_vs_obstacle_count(
    resistences,
    file_path,
):
    plt.figure(figsize=(10, 6))

    # Sort the data by obstacle count
    resistences = dict(sorted(resistences.items()))

    plt.plot(
        list(resistences.keys()),
        list(resistences.values()),
        "-o",
    )

    plt.xlabel("Cantidad de obstáculos")
    plt.ylabel("Resistencia (g/cm)")

    plt.grid(True)
    plt.savefig(file_path)
    plt.close()

def animate_simulation(config, obstacles, snapshots, file_path="animation.mp4"):
    fig, ax = plt.subplots(figsize=(10, 10))
    ax.set_xlim(0, config["length"])
    ax.set_ylim(0, config["width"])

    # Draw walls
    wall_bottom = plt.Line2D((0, config["length"]), (0, 0), color="black", lw=2)
    wall_top = plt.Line2D(
        (0, config["length"]), (config["width"], config["width"]), color="black", lw=2
    )

    ax.add_line(wall_bottom)
    ax.add_line(wall_top)

    # Create a list of circles for obstacles
    obstacle_circles = [
        plt.Circle((x, y), config["obstacle_radius"], color="red", alpha=0.5)
        for (x, y) in obstacles
    ]
    for circle in obstacle_circles:
        ax.add_artist(circle)

    # Create a list to hold particle circles
    particle_circles = []
    frames = len(snapshots)

    # Function to update the animation
    def update(frame):
        if frames > 20 and frame % (frames // 20) == 0:
            print(f"Progress: {frame / frames * 100:.1f}%")
        time = list(snapshots.keys())[frame]  # Get the time from the snapshot keys
        particles = snapshots[time]  # Get particles for this frame

        # Clear existing particle circles
        for circle in particle_circles:
            circle.remove()
        particle_circles.clear()

        # Add new particle circles for the current frame
        for x, y in particles:
            circle = plt.Circle(
                (x, y), config["particle_radius"], color="blue", alpha=0.7
            )
            particle_circles.append(circle)
            ax.add_artist(circle)

        return particle_circles

    # Create animation

    print(f"Animating {frames} frames...")
    ani = animation.FuncAnimation(fig, update, frames=frames, interval=200, blit=True)

    plt.gca().set_aspect("equal", adjustable="box")

    ani.save(file_path, writer="ffmpeg", fps=30)
