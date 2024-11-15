import subprocess

def load_discharges(file_path):
    discharges = []
    with open(file_path, 'r') as f:
        # Skip the first line as it contains the number of discharge times
        next(f)

        discharges = [float(line.strip()) for line in f]
    return discharges


def load_snapshots(file_path):
    snapshots = {}
    with open(file_path, 'r') as f:
        # Read the first line containing particle count and total snapshots
        header = f.readline().strip().split()
        particle_count = int(header[0])
        total_snapshots = int(header[1])

        # Parse each snapshot
        for _ in range(total_snapshots):
            time = float(f.readline().strip())
            particles = []

            for _ in range(particle_count):
                x, y = map(float, f.readline().strip().split())
                particles.append((x, y))

            snapshots[time] = particles

    return snapshots


def load_obstacles(file_path):
    obstacles = []
    with open(file_path, 'r') as f:
        # Skip the first line as it contains the number of obstacles
        next(f)
        # Read each obstacle's position
        obstacles = [tuple(map(float, line.strip().split())) for line in f]
    return obstacles


def load_config(file_path):
    config_keys = [
        "width", "length", "obstacle_count", "particle_count",
        "obstacle_radius", "particle_radius", "particle_mass",
        "acceleration", "normal_k", "tangential_k",
        "integration_step", "snapshot_step", "max_time", "seed"
    ]
    config = {}
    with open(file_path, 'r') as f:
        # Read each config value and assign it to the corresponding key
        for key in config_keys:
            config[key] = float(f.readline().strip())
    return config


def execute_granular_dynamics_jar(
        width, length, obstacle_count, particle_count,
        obstacle_radius, particle_radius, particle_mass,
        acceleration, normal_k, tangential_k,
        integration_step, snapshot_step, max_time, g,
        iteration, output_directory, jar_path="../target/granular-dynamics-1.0-jar-with-dependencies.jar"
):
    """
    Parameters:
    - width (float): Width of the environment.
    - length (float): Length of the environment.
    - obstacle_count (int): Number of obstacles.
    - particle_count (int): Number of particles.
    - obstacle_radius (float): Radius of the obstacles.
    - particle_radius (float): Radius of the particles.
    - particle_mass (float): Mass of the particles.
    - acceleration (float): Acceleration of the particles.
    - normal_k (float): Normal force constant.
    - tangential_k (float): Tangential force constant.
    - integration_step (float): Integration step.
    - snapshot_step (float): Snapshot step.
    - max_time (float): Max simulation time.
    - output_directory (str): Directory for output files.
    - jar_path (str): Path to the JAR file.
    """
    # unique dir with amount of obstacles, iteration, and acceleration
    output_directory = f"{output_directory}/obstacles_{obstacle_count}_iteration_{iteration}_acceleration_{acceleration}"

    command = [
        "java", "-jar", jar_path,
        "-W", str(width),
        "-L", str(length),
        "-M", str(obstacle_count),
        "-N", str(particle_count),
        "-R", str(obstacle_radius),
        "-r", str(particle_radius),
        "-m", str(particle_mass),
        "-A", str(acceleration),
        "-k_n", str(normal_k),
        "-k_t", str(tangential_k),
        "-dt", str(integration_step),
        "-dt2", str(snapshot_step),
        "-tf", str(max_time),
        "-g", str(g),
        "-out", output_directory
    ]

    try:
        print(f"[WORKER] - Running simulation, a={acceleration}, m={obstacle_count}, i={iteration}")
        subprocess.run(command, check=True, capture_output=True)
        print(f"[WORKER] - Simulation Finished, a={acceleration}, m={obstacle_count}, i={iteration}")
    except subprocess.CalledProcessError as e:
        print(f"[WORKER] - Error for a={acceleration}, m={obstacle_count}, i={iteration}: {e}")

    return output_directory
