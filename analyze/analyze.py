import numpy as np
import sys
import os
import json
import shutil
import concurrent.futures
import utils
import plots


def simulate(iterations, a_values, m_values, output_directory):
    results = []

    print("Executing Simulations")

    W = 40
    L = 140
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
    workers = 15

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
                acceleration,
                k_n,
                k_t,
                dt,
                dt2,
                tf,
                g,
                i,
                f"{output_directory}/simulations",
            )
            for acceleration in a_values
            for obstacle_count in m_values
            for i in range(iterations)
        ]

        jobs = len(futures)
        completed = 0

        for future in concurrent.futures.as_completed(futures):
            try:
                dir = future.result()
                print(f"[MAIN {completed+1}/{jobs}] - Simulation completed: {dir}")

                exit_times = utils.load_discharges(f"{dir}/discharges.txt")
                config = utils.load_config(f"{dir}/config.txt")

                results.append({"exit_times": exit_times, "config": config})

                completed += 1

            except Exception as e:
                print(f"[MAIN {completed+1}/{jobs}] - Error: {e}")

    # Save results json dump
    with open(f"{output_directory}/results.json", "w") as f:
        print("Saving results")
        json.dump(results, f)

    try:
        shutil.rmtree(f"{output_directory}/simulations")
    except Exception as e:
        print(f"Error: {e}")


def load_results(output_directory):
    with open(f"{output_directory}/results.json", "r") as f:
        return json.load(f)


def plot_equivalent_simulations(results, plot_directory):

    os.makedirs(f"{plot_directory}/equivalent_simulations", exist_ok=True)


    # Load results from equivalent simulations
    discharge_times = {}

    for result in results:
        exit_times = result["exit_times"]
        config = result["config"]

        key = (config["acceleration"], config["obstacle_count"])
        if key not in discharge_times:
            discharge_times[key] = []

        discharge_times[key].append(exit_times)

    for key, times in discharge_times.items():
        acceleration, obstacle_count = key
        file_name = f"{plot_directory}/equivalent_simulations/A_{acceleration}_M_{obstacle_count}.png"

        plots.plot_cumulative_discharges(
            times,
            file_name,
        )


def calculate_flow_rate(exit_times, steady_state_time):
    # Filtrar la fase de estado estacionario
    filtered_times = np.array(exit_times)[np.array(exit_times) >= steady_state_time]
    cumulative_particles = np.arange(1, len(filtered_times) + 1)

    # Q = deltay / deltax
    slope = (cumulative_particles[-1] - cumulative_particles[0]) / (
        filtered_times[-1] - filtered_times[0]
    )

    return slope

def calculate_resistence(flow_rates, accelerations, mass):

    # Metodo teorica 0, Q = f(a,R) = (a * m ) / R
    r_values = np.linspace(1.5, 9.5, 800)
    squared_errors = {}

    best_resistence = None

    for r in r_values:
        squared_error = 0
        for a, q in zip(accelerations, flow_rates):
            predicted_q = ((a - accelerations[0]) * mass) / r + flow_rates[0]
            squared_error += (q - predicted_q) ** 2

        squared_errors[r] = squared_error

        if best_resistence is None or squared_error < squared_errors[best_resistence]:
            best_resistence = r

    return best_resistence, squared_errors




def plot_flow_rate_analysis(results, plot_directory):
    flow_rates = {}

    if len(results) == 0:
        print("Error: no results to analyze")
        return

    mass = results[0]["config"]["particle_mass"]

    for result in results:
        config = result["config"]
        obstacles = config["obstacle_count"]
        max_time = config["max_time"]

        exit_times = result["exit_times"]
        if len(exit_times) == 0:
            print(
                f"Error: empty exit times for {obstacles} obstacles, {config['acceleration']} acceleration, {config['max_time']} max time"
            )
            continue

        flow_rate = calculate_flow_rate(exit_times, max_time / 2)

        if obstacles not in flow_rates:
            flow_rates[obstacles] = {}

        acceleration = config["acceleration"]

        if acceleration not in flow_rates[obstacles]:
            flow_rates[obstacles][acceleration] = []

        flow_rates[obstacles][acceleration].append(flow_rate)

    mean_flow_rates = {}
    std_flow_rates = {}

    for obstacles, rates in flow_rates.items():
        mean_flow_rates[obstacles] = {}
        std_flow_rates[obstacles] = {}
        for acceleration, rates in rates.items():
            mean_flow_rates[obstacles][acceleration] = np.mean(rates)
            std_flow_rates[obstacles][acceleration] = np.std(rates)

    resitences = {}


    os.makedirs(f"{plot_directory}/best_resistence", exist_ok=True)

    for obstacle_count, mean_flow_rate in mean_flow_rates.items():
        accelerations = list(mean_flow_rate.keys())
        mean_flow_rate = list(mean_flow_rate.values())
        std_flow_rate = list(std_flow_rates[obstacle_count].values())

        # Sort the data by acceleration
        accelerations, mean_flow_rate = zip(*sorted(zip(accelerations, mean_flow_rate)))

        best_resistence, squared_errors = calculate_resistence(mean_flow_rate, accelerations, mass)

        os.makedirs(f"{plot_directory}/best_resistence/M_{obstacle_count}", exist_ok=True)

        plots.plot_flow_rate_with_best_resistence_vs_acceleration(
            accelerations,
            mean_flow_rate,
            std_flow_rate,
            best_resistence,
            mass,
            f"{plot_directory}/best_resistence/M_{obstacle_count}/best_resistence.png",
        )

        plots.plot_cuadriatic_error_vs_resistence(
            squared_errors,
            best_resistence,
            f"{plot_directory}/best_resistence/M_{obstacle_count}/cuadratic_error.png",
        )

        resitences[obstacle_count] = best_resistence
        


    os.makedirs(f"{plot_directory}/analysis", exist_ok=True)

    plots.plot_resistence_vs_obstacle_count(
        resitences,
        f"{plot_directory}/analysis/resistence_vs_obstacle_count.png",
    )

    # Only the first, third and fifth obstacle count
    obstacle_counts = list(mean_flow_rates.keys())
    selected_obstacle_counts = obstacle_counts[::2]


    plots.plot_flow_rate_vs_acceleration(
        {k: mean_flow_rates[k] for k in selected_obstacle_counts},
        {k: std_flow_rates[k] for k in selected_obstacle_counts},
        f"{plot_directory}/analysis/flow_rate_vs_acceleration.png",
    )

    # mean  flow rates: [obstacle_count] -> [acceleration] -> flow rate
    # now i want flow rates: [axxeleration] -> [obstacle_count] -> flow rate

    inverted_mean_flow_rates = {}
    inverted_std_flow_rates = {}

    for obstacle_count, mean_flow_rate in mean_flow_rates.items():
        for acceleration, rate in mean_flow_rate.items():
            if acceleration not in inverted_mean_flow_rates:
                inverted_mean_flow_rates[acceleration] = {}
                inverted_std_flow_rates[acceleration] = {}

            inverted_mean_flow_rates[acceleration][obstacle_count] = rate
            inverted_std_flow_rates[acceleration][obstacle_count] = std_flow_rates[
                obstacle_count
            ][acceleration]

    accelerations = list(inverted_mean_flow_rates.keys())
    selected_accelerations = accelerations[::2]

    inverted_mean_flow_rates = {
        k: inverted_mean_flow_rates[k] for k in selected_accelerations
    }
    inverted_std_flow_rates = {
        k: inverted_std_flow_rates[k] for k in selected_accelerations
    }

    plots.plot_flow_rate_vs_obstacle_count(
        inverted_mean_flow_rates,
        inverted_std_flow_rates,
        f"{plot_directory}/analysis/flow_rate_vs_obstacle_count.png",
    )

def animate(output_directory):

    combinations = [
        (1.6, 60), (5.0, 60), 
        (1.6, 40), (1.6, 80)
    ]

    W = 40
    L = 140
    N = 100
    R = 1
    r = 1
    mass = 1
    k_n = 250
    g = k_n / 100
    k_t = 500
    dt = 0.0005
    dt2 = 0.05
    tf = 1000

    os.makedirs(f"{output_directory}/simulations", exist_ok=True)
    os.makedirs(f"{output_directory}/animations", exist_ok=True)

    for acceleration, obstacle_count in combinations:

        print(f"Simulating A: {acceleration} M: {obstacle_count}")

        directory = utils.execute_granular_dynamics_jar(
            W,
            L,
            obstacle_count,
            N,
            R,
            r,
            mass,
            acceleration,
            k_n,
            k_t,
            dt,
            dt2,
            tf,
            g,
            0,
            f"{output_directory}/simulations",
        )

        snapshots = utils.load_snapshots(f"{directory}/snapshots.txt")
        obstacles = utils.load_obstacles(f"{directory}/obstacles.txt")
        config = utils.load_config(f"{directory}/config.txt")

        print(f"Animating A: {acceleration} M: {obstacle_count}")

        plots.animate_simulation(config, obstacles, snapshots, f"{output_directory}/animations/A_{acceleration}_M_{obstacle_count}.mp4")


    try:
        shutil.rmtree(f"{output_directory}/simulations")
    except Exception as e:
        print(f"Error: {e}")



if __name__ == "__main__":

    # python analyze.py [generate|plot] directory
    args = sys.argv

    if len(args) < 3:
        print("Usage: python analyze.py [generate|plot|animate] directory")
        exit()

    if args[1] == "generate":
        output_directory = args[2]
        num_simulations = 5

        start_A = 0.5
        stop_A = 5
        start_M = 40
        stop_M = 80
        qty_steps = 5
        iterations = 5

        a_values = np.linspace(start_A, stop_A, qty_steps)
        m_values = np.linspace(start_M, stop_M, qty_steps, dtype=int)

        simulate(iterations, a_values, m_values, f"{output_directory}")
    elif args[1] == "plot":
        plot_directory = args[2]

        results = load_results(plot_directory)

        plot_directory = f"{plot_directory}/plots"

        plot_flow_rate_analysis(results, plot_directory)
        plot_equivalent_simulations(results, plot_directory)
    elif args[1] == "animate":
        animate(args[2])
    else:
        print("Usage: python analyze.py [generate|plot|animate] directory")
        exit()
