import numpy as np
from scipy.stats import linregress
import utils
import plots

output_directory = 'data/analysis'
plot_directory = 'data/plots'

W = 20
L = 70
M = 40
N = 100
R = 1
r = 1
m = 1
k_n = 250
k_t = 500
dt = 0.001
dt2 = 0.01
tf = 50

def equivalent_simulations():
    A = 1

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



def calculate_flow_rate(exit_times, steady_state_time):
    # Filtrar la fase de estado estacionario
    filtered_times = np.array(exit_times)[np.array(exit_times) >= steady_state_time]
    cumulative_particles = np.arange(1, len(filtered_times) + 1)

    # Regresión lineal para estimar el caudal Q en estado estacionario
    slope, _, _, _, _ = linregress(filtered_times, cumulative_particles)
    return slope  # El valor de Q



def calculate_flow_rate_vs_acceleration():
    A_values = np.linspace(0.005, 0.05, 4)
    mean_flow_rates = []
    std_flow_rates = []

    for A in A_values:
        flow_rates = []
        for _ in range(5):
            # Ejecutar la simulación
            utils.execute_granular_dynamics_jar(
                W, L, M, N, R, r, m, A, k_n, k_t, dt, dt2, tf, output_directory
            )

            # Cargar los tiempos de salida
            exit_times = utils.load_discharges(f'{output_directory}/discharges.txt')

            # Calcular el caudal
            flow_rate = calculate_flow_rate(exit_times, tf / 2)
            flow_rates.append(flow_rate)

        # Calcular la media y la desviación estándar de los caudales
        mean_flow_rates.append(np.mean(flow_rates))
        std_flow_rates.append(np.std(flow_rates))

    # Graficar Q vs A0 con barras de error
    plots.plot_flow_rate_vs_acceleration(A_values, mean_flow_rates, std_flow_rates, f'{plot_directory}/flow_rate_vs_acceleration.png')



if __name__ == '__main__':
    # discharge_times = utils.load_discharges(f'{output_directory}/discharges.txt')
    # obstacles = utils.load_obstacles(f'{output_directory}/obstacles.txt')
    # snapshots = utils.load_snapshots(f'{output_directory}/snapshots.txt')
    # config = utils.load_config(f'{output_directory}/config.txt')
    #
    # # Get the first snapshot's particle positions
    # first_snapshot = snapshots[next(iter(snapshots))]  # Get the first snapshot (the one with the smallest time)
    #
    # # Plot the initial state
    # plots.plot_initial_state(config, obstacles, first_snapshot, f'{plot_directory}/initial_state.png')

    equivalent_simulations()
    calculate_flow_rate_vs_acceleration()