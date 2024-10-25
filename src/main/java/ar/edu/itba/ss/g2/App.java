package ar.edu.itba.ss.g2;

import ar.edu.itba.ss.g2.config.ArgParser;
import ar.edu.itba.ss.g2.config.Config;
import ar.edu.itba.ss.g2.generation.ObstacleGenerator;
import ar.edu.itba.ss.g2.generation.ParticleGenerator;
import ar.edu.itba.ss.g2.model.Particle;

import java.util.List;
import java.util.Random;

public class App {
    public static void main(String[] args) {

        ArgParser parser = new ArgParser(args);
        Config config = parser.parse();

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
    }
}
