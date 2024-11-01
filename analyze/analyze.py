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


def simulate_equivalent_simulations(num_simulations: int):
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
                f'{output_directory}/equivalent/sim_{i}',
            )
            for i in range(num_simulations)
        ]

        for future in concurrent.futures.as_completed(futures):
            try:
                future.result()
            except Exception as e:
                print(f"Error: {e}")


def plot_equivalent_simulations(num_simulations: int):
    # Load results from equivalent simulations
    discharge_times = []

    for i in range(num_simulations):
        exit_times = utils.load_discharges(f"{output_directory}/equivalent/sim_{i}/discharges.txt")
        discharge_times.append(exit_times)

    # Plot the cumulative discharges in one graph
    plots.plot_cumulative_discharges(
        discharge_times, f"{plot_directory}/equivalent_simulations.png"
    )


def calculate_flow_rate(exit_times, steady_state_time):
    # Filtrar la fase de estado estacionario
    filtered_times = np.array(exit_times)[np.array(exit_times) >= steady_state_time]
    cumulative_particles = np.arange(1, len(filtered_times) + 1)

    # Regresión lineal para estimar el caudal Q en estado estacionario
    slope, _, _, _, _ = linregress(filtered_times, cumulative_particles)
    return slope  # El valor de Q


def simulate_flow_rate_vs_acceleration(start_A, stop_A, qty_steps, num_simulations):
    A_values = np.linspace(start_A, stop_A, qty_steps)

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
                f'{output_directory}/flow_rate_vs_acceleration/A_{a}/sim_{i}',
            )
            for i in range(num_simulations)
            for a in A_values
        ]

        for future in concurrent.futures.as_completed(futures):
            try:
                future.result()
            except Exception as e:
                print(f"Error: {e}")


def plot_flow_rate_vs_acceleration(start_A, stop_A, qty_steps, num_simulations):
    A_values = np.linspace(start_A, stop_A, qty_steps)

    mean_flow_rates = []
    std_flow_rates = []

    for a in A_values:
        flow_rates = []
        for i in range(num_simulations):
            dir = f'{output_directory}/flow_rate_vs_acceleration/A_{a}/sim_{i}'
            exit_times = utils.load_discharges(f"{dir}/discharges.txt")

            config = utils.load_config(f"{dir}/config.txt")
            max_time = config["max_time"]

            flow_rate = calculate_flow_rate(exit_times, max_time / 2)

            flow_rates.append(flow_rate)

        mean_flow_rates.append(np.mean(flow_rates))
        std_flow_rates.append(np.std(flow_rates))

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



def simulate_resistence_vs_obstacles(start_M, stop_M, qty_steps, num_simulations):
    M_values = np.linspace(start_M, stop_M, qty_steps, dtype=int)

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
                f'{output_directory}/resistence_vs_obstacles/M_{obstacle_count}/sim_{i}',
            )
            for i in range(num_simulations)
            for obstacle_count in M_values
        ]

        for future in concurrent.futures.as_completed(futures):
            try:
                future.result()
            except Exception as e:
                print(f"Error: {e}")


def plot_flow_rate_and_resistence_vs_obstacles(start_M, stop_M, qty_steps, num_simulations):
    M_values = np.linspace(start_M, stop_M, qty_steps, dtype=int)

    mean_flow_rates = []
    std_flow_rates = []
    mean_resistences = []
    std_resistences = []

    for M in M_values:
        flow_rates = []
        resistences = []
        for i in range(num_simulations):
            dir = f"{output_directory}/resistence_vs_obstacles/M_{M}/sim_{i}"

            exit_times = utils.load_discharges(f"{dir}/discharges.txt")

            config = utils.load_config(f"{dir}/config.txt")
            obstacle_count = config["obstacle_count"]
            particle_mass = config["particle_mass"]
            acceleration = config["acceleration"]
            max_time = config["max_time"]

            flow_rate = calculate_flow_rate(exit_times, max_time / 2)
            flow_rates.append(flow_rate)


            resistence = (particle_mass * acceleration) / flow_rate
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


def delete_output_directory():
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
    
    num_simulations = 5

    simulate_equivalent_simulations(num_simulations)
    plot_equivalent_simulations(num_simulations)

    start_A = 0.5
    stop_A = 5
    qty_steps = 4

    simulate_flow_rate_vs_acceleration(start_A, stop_A, qty_steps, num_simulations)
    plot_flow_rate_vs_acceleration(start_A, stop_A, qty_steps, num_simulations)

    start_M = 40
    stop_M = 80

    simulate_resistence_vs_obstacles(start_M, stop_M, qty_steps, num_simulations)
    plot_flow_rate_and_resistence_vs_obstacles(start_M, stop_M, qty_steps, num_simulations)

    # delete_output_directory()