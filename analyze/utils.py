
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
        "integration_step", "snapshot_step", "max_time"
    ]
    config = {}
    with open(file_path, 'r') as f:
        # Read each config value and assign it to the corresponding key
        for key in config_keys:
            config[key] = float(f.readline().strip())
    return config
