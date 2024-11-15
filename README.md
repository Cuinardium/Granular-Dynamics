# Granular Dynamics Simulation

This project is a Command Line Interface (CLI) tool designed to simulate granular dynamics in a two-dimensional environment. The simulation studies how particles interact under specified physical constraints, such as obstacle placement, particle properties, and applied forces.

![animation_speeder](https://github.com/user-attachments/assets/30dc72ec-556e-4677-b2cd-3465c790d573)

## Requirements

- Java 17 or higher
- Maven

## Building the Project

To build the project, navigate to the project directory and use Maven:

```bash
mvn clean package
```

The resulting JAR file will be located in the `target` directory.

## Usage

To execute the program, use the following command:

```bash
java -jar granular-dynamics-1.0-SNAPSHOT-jar-with-dependencies.jar [options]
```

### Options

| Short | Long                  | Argument          | Description                                                |
|-------|-----------------------|-------------------|------------------------------------------------------------|
| -h    | --help               | (none)            | Show help information and usage instructions.              |
| -out  | --output             | `<directory>`     | Output directory where results will be stored.             |
| -s    | --seed               | `<long>`          | Seed for the random number generator.                      |
| -W    | --width              | `<double>`        | Width of the simulation area.                              |
| -L    | --length             | `<double>`        | Length of the simulation area.                             |
| -M    | --obstacle-count     | `<int>`           | Number of obstacles in the environment.                    |
| -N    | --particle-count     | `<int>`           | Number of particles in the simulation.                     |
| -R    | --obstacle-radius    | `<double>`        | Radius of each obstacle.                                   |
| -r    | --particle-radius    | `<double>`        | Radius of each particle.                                   |
| -m    | --particle-mass      | `<double>`        | Mass of each particle.                                     |
| -A    | --acceleration       | `<double>`        | Acceleration acting on particles.                          |
| --k_n | --normal-k           | `<double>`        | Normal force constant.                                     |
| --k_t | --tangential-k       | `<double>`        | Tangential force constant.                                 |
| -dt   | --integration-step   | `<double>`        | Time step for integration.                                 |
| -dt2  | --snapshot-step      | `<double>`        | Time interval between snapshots.                           |
| -tf   | --max-time           | `<double>`        | Total simulation time.                                     |

## Output File Format

The output files will be saved in the specified output directory and follow a specific format:

### `config.txt`

This file contains the static parameters of the simulation. Example:

```txt
10.0  
20.0  
5  
100  
0.5  
0.1  
0.01  
9.8  
1.0  
1.0  
0.01  
0.1  
10.0  
42 
``` 

Order of parameters:  
- Width of the simulation area  
- Length of the simulation area  
- Number of obstacles  
- Number of particles  
- Radius of obstacles  
- Radius of particles  
- Mass of particles  
- Acceleration  
- Normal force constant  
- Tangential force constant  
- Time step for integration  
- Time interval for snapshots  
- Total simulation time  
- Seed for random number generator  

### `obstacles.txt`

This file lists the positions of obstacles. Example:

```txt
5  
1.00000 1.00000  
3.00000 3.00000  
5.00000 5.00000  
7.00000 7.00000  
9.00000 9.00000
```

- The first line contains the total number of obstacles.  
- Each subsequent line contains the `x` and `y` coordinates of an obstacle.  

### `discharges.txt`

This file contains the times when particles exit the simulation boundaries. Example:

```txt
3  
2.50000  
5.30000  
7.80000
```

- The first line contains the total number of discharges.  
- Each subsequent line lists the discharge time of a particle.  

### `snapshots.txt`

This file contains the particle positions at each snapshot. Example:

```txt
100 10  
0.10000  
0.00000 0.00000  
1.00000 1.00000
...  
```

- The first line contains the total number of particles and snapshots.  
- Each block starts with the snapshot time followed by the positions of all particles (`x` and `y`).  

## Analysis and Animation
This project also includes a set of analysis and visualization tools designed to process the simulation results and generate animations:

1. Simulate: The simulation function runs a set of granular dynamics simulations using various acceleration and obstacle count values. It performs the simulations in parallel using multiple threads, and the results are stored in a JSON format containing exit times and configuration data.
2. Plot: The plot functions visualizes the flow rate and resistance analysis of the simulate results file.
3. Animation: The animate function generates animations of the granular dynamics simulations, visualizing how the system evolves over time. These animations are saved as .mp4 files and can be used for a detailed, visual understanding of the system's behavior.

### Usage
You can execute the analysis and animation tasks using the following commands in the `analyze` directory:

- Generate Simulations: `python analyze.py generate <output_directory>`
- Plot Results: `python analyze.py plot <directory_with_results>`
- Animate Simulations: `python analyze.py animate <output_directory>`
