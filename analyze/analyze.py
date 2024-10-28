import numpy as np
from scipy.stats import linregress
import utils
import plots

output_directory = 'data/analysis'
plot_directory = 'data/plots'

A = 1
W = 40
L = 140
M = 80
N = 100
R = 1
r = 1
m = 1
k_n = 250
g = k_n / 100
k_t = 500
dt = 0.001
dt2 = 0.01
tf = 10

def equivalent_simulations():
    discharge_times = []
    for i in range(5):
        # Execute the simulation
        utils.execute_granular_dynamics_jar(
            W, L, M, N, R, r, m, A, k_n, k_t, dt, dt2, tf, g, output_directory
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



def flow_rate_and_resistence_vs_acceleration(start_A, stop_A, qty_steps):
    A_values = np.linspace(start_A, stop_A, qty_steps)
    mean_flow_rates = []
    std_flow_rates = []
    mean_resistences = []
    std_resistences = []

    for A in A_values:
        flow_rates = []
        resistences = []
        for _ in range(5):
            # Ejecutar la simulación
            utils.execute_granular_dynamics_jar(
                W, L, M, N, R, r, m, A, k_n, k_t, dt, dt2, tf, g, output_directory
            )

            # Cargar los tiempos de salida
            exit_times = utils.load_discharges(f'{output_directory}/discharges.txt')

            # Calcular el caudal
            flow_rate = calculate_flow_rate(exit_times, tf / 2)
            flow_rates.append(flow_rate)

            # Calcular la resistencia
            resistence = (m * A) / flow_rate
            resistences.append(resistence)

        # Calcular la media y la desviación estándar de los caudales
        mean_flow_rates.append(np.mean(flow_rates))
        std_flow_rates.append(np.std(flow_rates))

        # Calcular la media y la desviación estándar de las resistencias
        mean_resistences.append(np.mean(resistences))
        std_resistences.append(np.std(resistences))

    # Aceleracion en m/s²
    A_values = A_values / 100

    # Graficar Q vs A0 con barras de error
    plots.plot_X_vs_Y(A_values, mean_flow_rates, std_flow_rates, f'{plot_directory}/flow_rate_vs_acceleration.png', "Aceleración (m/s²)", "Caudal (partículas/s)")

    # Graficar R vs A0 con barras de error
    plots.plot_X_vs_Y(A_values, mean_resistences, std_resistences, f'{plot_directory}/resistence_vs_acceleration.png', "Aceleración (m/s²)", "Resistencia (kg/s)")


def flow_rate_and_resistence_vs_obstacles(start_M, stop_M, qty_steps):
    M_values = np.linspace(start_M, stop_M, qty_steps, dtype=int)

    mean_flow_rates = []
    std_flow_rates = []
    mean_resistences = []
    std_resistences = []

    for M in M_values:
        flow_rates = []
        resistences = []
        for _ in range(5):
            # Ejecutar la simulación
            utils.execute_granular_dynamics_jar(
                W, L, M, N, R, r, m, A, k_n, k_t, dt, dt2, tf, g, output_directory
            )

            # Cargar los tiempos de salida
            exit_times = utils.load_discharges(f'{output_directory}/discharges.txt')

            # Calcular el caudal
            flow_rate = calculate_flow_rate(exit_times, tf / 2)
            flow_rates.append(flow_rate)

            # Calcular la resistencia
            resistence = (m * A) / flow_rate
            resistences.append(resistence)

        # Calcular la media y la desviación estándar de los caudales
        mean_flow_rates.append(np.mean(flow_rates))
        std_flow_rates.append(np.std(flow_rates))

        # Calcular la media y la desviación estándar de las resistencias
        mean_resistences.append(np.mean(resistences))
        std_resistences.append(np.std(resistences))

    # Graficar Q vs M con barras de error
    plots.plot_X_vs_Y(M_values, mean_flow_rates, std_flow_rates, f'{plot_directory}/flow_rate_vs_obstacles.png', "Número de obstáculos", "Caudal (partículas/s)")

    # Graficar R vs M con barras de error
    plots.plot_X_vs_Y(M_values, mean_resistences, std_resistences, f'{plot_directory}/resistence_vs_obstacles.png', "Número de obstáculos", "Resistencia (kg/s)")



if __name__ == '__main__':
    equivalent_simulations()
    flow_rate_and_resistence_vs_acceleration(0.5, 5, 4)
    flow_rate_and_resistence_vs_obstacles(80, 120, 4)