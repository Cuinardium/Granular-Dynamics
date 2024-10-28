package ar.edu.itba.ss.g2;

import ar.edu.itba.ss.g2.config.ArgParser;
import ar.edu.itba.ss.g2.config.Config;
import ar.edu.itba.ss.g2.generation.ObstacleGenerator;
import ar.edu.itba.ss.g2.generation.ParticleGenerator;
import ar.edu.itba.ss.g2.model.Particle;
import ar.edu.itba.ss.g2.simulation.Simulation;
import ar.edu.itba.ss.g2.util.FileUtil;

import java.util.List;
import java.util.Random;

public class App {
  public static void main(String[] args) {

    ArgParser parser = new ArgParser(args);
    Config config = parser.parse();

    if (config == null) {
      System.err.println("Error while parsing arguments");
      System.exit(1);
    }

    // TODO: seed
    Random random = new Random();

    ObstacleGenerator obstacleGenerator =
        new ObstacleGenerator(
            config.getWidth(),
            config.getLength(),
            config.getObstacleCount(),
            config.getObstacleRadius(),
            random);

    List<Particle> obstacles = obstacleGenerator.generate();

    ParticleGenerator particleGenerator =
        new ParticleGenerator(
            config.getWidth(),
            config.getLength(),
            config.getParticleCount(),
            config.getParticleRadius(),
            config.getParticleMass(),
            config.getAcceleration(),
            obstacles,
            random);

    List<Particle> particles = particleGenerator.generate();

    Simulation simulation = new Simulation(
        particles,
        obstacles,
        config.getWidth(),
        config.getLength(),
        config.getAcceleration(),
        config.getNormalK(),
        config.getTangentialK(),
        config.getIntegrationStep(),
        config.getSnapshotStep(),
        config.getMaxTime());


    simulation.run();

    List<List<Particle>> snapshots = simulation.getSnapshots();
    List<Double> dischargeTimes = simulation.getDischargeTimes();

    try {
      FileUtil.serializeConfig(config, config.getOutputDirectory());
      FileUtil.serializeObstacles(obstacles, config.getOutputDirectory());
      FileUtil.serializeDischarges(dischargeTimes, config.getOutputDirectory());
      FileUtil.serializeSnapshots(snapshots, config.getSnapshotStep(), config.getOutputDirectory());
    } catch (Exception e) {
      System.err.println("Error while serializing output");
      System.exit(1);
    }

    System.exit(0);
  }
}
