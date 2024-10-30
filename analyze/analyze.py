import numpy as np
import shutil
from scipy.stats import linregress
import concurrent.futures
import utils
import plots

output_directory = "data/analysis"
plot_directory = "data/plots"

A = 1
W = 40
L = 140
M = 60
N = 100
R = 1
r = 1
mass = 1
k_n = 250
g = k_n / 100
k_t = 500
dt = 0.001
dt2 = 10
tf = 1000
workers = 16


def equivalent_simulations():
    discharge_times = []

    with concurrent.futures.ThreadPoolExecutor(max_workers=workers) as executor:
        futures = [
            executor.submit(
                utils.execute_granular_dynamics_jar,
                W,
                L,
                M,
                N,
                R,
                r,
                mass,
                A,
                k_n,
                k_t,
                dt,
                dt2,
                tf,
                g,
                i,
                output_directory,
            )
            for i in range(5)
        ]

        for future in concurrent.futures.as_completed(futures):
            try:
                dir = future.result()

                exit_times = utils.load_discharges(f"{dir}/discharges.txt")

                discharge_times.append(exit_times)

            except Exception as e:
                print(f"Error: {e}")

    # Plot the cumulative discharges in one graph
    plots.plot_cumulative_discharges(
        discharge_times, f"{plot_directory}/equivalent_simulations.png"
    )

    try:
        shutil.rmtree(output_directory)
    except Exception as e:
        print(f"Error: {e}")


def calculate_flow_rate(exit_times, steady_state_time):
    # Filtrar la fase de estado estacionario
    filtered_times = np.array(exit_times)[np.array(exit_times) >= steady_state_time]
    cumulative_particles = np.arange(1, len(filtered_times) + 1)

    # Regresión lineal para estimar el caudal Q en estado estacionario
    slope, _, _, _, _ = linregress(filtered_times, cumulative_particles)
    return slope  # El valor de Q


def flow_rate_and_resistence_vs_acceleration(start_A, stop_A, qty_steps):
    A_values = np.linspace(start_A, stop_A, qty_steps)
    mean_flow_rates = []
    std_flow_rates = []
    mean_resistences = []
    std_resistences = []

    with concurrent.futures.ThreadPoolExecutor(max_workers=workers) as executor:
        futures = [
            executor.submit(
                utils.execute_granular_dynamics_jar,
                W,
                L,
                M,
                N,
                R,
                r,
                mass,
                a,
                k_n,
                k_t,
                dt,
                dt2,
                tf,
                g,
                i,
                output_directory,
            )
            for i in range(5)
            for a in A_values
        ]

        results = {}
        for future in concurrent.futures.as_completed(futures):
            try:
                dir = future.result()

                exit_times = utils.load_discharges(f"{dir}/discharges.txt")

                config = utils.load_config(f"{dir}/config.txt")
                acceleration = config["acceleration"]
                particle_mass = config["particle_mass"]
                max_time = config["max_time"]

                flow_rate = calculate_flow_rate(exit_times, max_time / 2)

                resistence = (particle_mass * acceleration) / flow_rate

                if acceleration not in results:
                    results[acceleration] = [(flow_rate, resistence)]
                else:
                    results[acceleration].append((flow_rate, resistence))

            except Exception as e:
                print(f"Error: {e}")

    mean_flow_rates = []
    std_flow_rates = []
    mean_resistences = []
    std_resistences = []

    for a in A_values:
        flow_rates = []
        resistences = []
        for flow_rate, resistence in results[a]:
            flow_rates.append(flow_rate)
            resistences.append(resistence)

        mean_flow_rates.append(np.mean(flow_rates))
        std_flow_rates.append(np.std(flow_rates))
        mean_resistences.append(np.mean(resistences))
        std_resistences.append(np.std(resistences))

    A_values = A_values / 100

    # Graficar Q vs A0 con barras de error
    plots.plot_X_vs_Y(
        A_values,
        mean_flow_rates,
        std_flow_rates,
        f"{plot_directory}/flow_rate_vs_acceleration.png",
        "Aceleración (m/s²)",
        "Caudal (partículas/s)",
    )
    plots.plot_X_vs_Y(
        A_values,
        mean_resistences,
        std_resistences,
        f"{plot_directory}/resistence_vs_acceleration.png",
        "Aceleración (m/s²)",
        "Resistencia (kg/s)",
    )

    try:
        shutil.rmtree(output_directory)
    except Exception as e:
        print(f"Error: {e}")


def flow_rate_and_resistence_vs_obstacles(start_M, stop_M, qty_steps):
    M_values = np.linspace(start_M, stop_M, qty_steps, dtype=int)

    mean_flow_rates = []
    std_flow_rates = []
    mean_resistences = []
    std_resistences = []

    with concurrent.futures.ThreadPoolExecutor(max_workers=workers) as executor:
        futures = [
            executor.submit(
                utils.execute_granular_dynamics_jar,
                W,
                L,
                obstacle_count,
                N,
                R,
                r,
                mass,
                A,
                k_n,
                k_t,
                dt,
                dt2,
                tf,
                g,
                i,
                output_directory,
            )
            for i in range(5)
            for obstacle_count in M_values
        ]

        results = {}
        for future in concurrent.futures.as_completed(futures):
            try:
                dir = future.result()

                exit_times = utils.load_discharges(f"{dir}/discharges.txt")

                config = utils.load_config(f"{dir}/config.txt")
                obstacle_count = config["obstacle_count"]
                particle_mass = config["particle_mass"]
                acceleration = config["acceleration"]
                max_time = config["max_time"]

                flow_rate = calculate_flow_rate(exit_times, max_time / 2)

                resistence = (particle_mass * acceleration) / flow_rate

                if obstacle_count not in results:
                    results[obstacle_count] = [(flow_rate, resistence)]
                else:
                    results[obstacle_count].append((flow_rate, resistence))

            except Exception as e:
                print(f"Error: {e}")

    mean_flow_rates = []
    std_flow_rates = []
    mean_resistences = []
    std_resistences = []

    for obstacle_count in M_values:
        flow_rates = []
        resistences = []
        for flow_rate, resistence in results[obstacle_count]:
            flow_rates.append(flow_rate)
            resistences.append(resistence)

        mean_flow_rates.append(np.mean(flow_rates))
        std_flow_rates.append(np.std(flow_rates))
        mean_resistences.append(np.mean(resistences))
        std_resistences.append(np.std(resistences))

    # Graficar Q vs M con barras de error
    plots.plot_X_vs_Y(
        M_values,
        mean_flow_rates,
        std_flow_rates,
        f"{plot_directory}/flow_rate_vs_obstacles.png",
        "Número de obstáculos",
        "Caudal (partículas/s)",
    )

    # Graficar R vs M con barras de Erroe
    plots.plot_X_vs_Y(
        M_values,
        mean_resistences,
        std_resistences,
        f"{plot_directory}/resistence_vs_obstacles.png",
        "Número de obstáculos",
        "Resistencia (kg/s)",
    )

    try:
        shutil.rmtree(output_directory)
    except Exception as e:
        print(f"Error: {e}")


if __name__ == "__main__":
    """config = utils.load_config('data/default/config.txt')"""
    """ snapshots2 = utils.load_snapshots('data/default/snapshots.txt') """
    """ obstacles = utils.load_obstacles('data/default/obstacles.txt') """

    # plots.animate_simulation(config, obstacles, snapshots, 'data/default/animation.mp4')

    # data/cim
    """ config = utils.load_config('data/cim/config.txt') """
    """ snapshots1 = utils.load_snapshots('data/cim/snapshots.txt') """
    """ obstacles = utils.load_obstacles('data/cim/obstacles.txt') """

    # plots.animate_simulation(config, obstacles, snapshots, 'data/cim/animation.mp4')

    # plots.animate_comparison(config, obstacles, snapshots1, snapshots2, "data/comparison.mp4")
    equivalent_simulations()
    flow_rate_and_resistence_vs_acceleration(0.5, 5, 4)
    flow_rate_and_resistence_vs_obstacles(40, 80, 4)
