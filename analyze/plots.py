import matplotlib.pyplot as plt
import matplotlib.animation as animation
import numpy as np


def plot_cumulative_discharges(discharge_times, file_path="discharges.png"):
    discharge_times = sorted(discharge_times)

    # Generate cumulative discharge count
    cumulative_discharges = np.arange(1, len(discharge_times) + 1)

    # Plot cumulative discharges over time
    plt.figure(figsize=(10, 6))
    plt.plot(discharge_times, cumulative_discharges, marker="o", linestyle="-")
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
        for (x, y) in particles:
            circle = plt.Circle((x, y), config['particle_radius'], color='blue', alpha=0.7)
            particle_circles.append(circle)
            ax.add_artist(circle)

        return particle_circles
    # Create animation

    print(f"Animating {frames} frames...")
    ani = animation.FuncAnimation(
        fig, update, frames=frames, interval=200, blit=True
    )

    plt.gca().set_aspect("equal", adjustable="box")

    ani.save(file_path, writer="ffmpeg", fps=5)
