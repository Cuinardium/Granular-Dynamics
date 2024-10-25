package ar.edu.itba.ss.g2.util;

import ar.edu.itba.ss.g2.config.Config;
import ar.edu.itba.ss.g2.model.Particle;

import java.io.BufferedWriter;
import java.io.File;
import java.io.FileWriter;
import java.io.IOException;
import java.util.*;

public class FileUtil {

    private FileUtil() {
        throw new RuntimeException("Util class");
    }

    public static void serializeConfig(Config config, String directory) throws IOException {

        File dir = new File(directory);
        if (!dir.exists()) {
            dir.mkdirs();
        }

        try (FileWriter writer = new FileWriter(directory + "/config.txt")) {
            writer.write(config.getWidth() + "\n");
            writer.write(config.getLength() + "\n");
            writer.write(config.getObstacleCount() + "\n");
            writer.write(config.getParticleCount() + "\n");
            writer.write(config.getObstacleRadius() + "\n");
            writer.write(config.getParticleRadius() + "\n");
            writer.write(config.getParticleMass() + "\n");
            writer.write(config.getAcceleration() + "\n");
            writer.write(config.getNormalK() + "\n");
            writer.write(config.getTangentialK() + "\n");
            writer.write(config.getIntegrationStep() + "\n");
            writer.write(config.getSnapshotStep() + "\n");
            writer.write(config.getMaxTime() + "\n");
        }
    }

    public static void serializeObstacles(List<Particle> obstacles, String directory)
            throws IOException {

        File dir = new File(directory);
        if (!dir.exists()) {
            dir.mkdirs();
        }

        try (FileWriter writer = new FileWriter(directory + "/obstacles.txt")) {
            writer.write(obstacles.size() + '\n');

            for (Particle obstacle : obstacles) {
                writer.write(String.format("%.5f %.5f\n", obstacle.getX(), obstacle.getY()));
            }
        }
    }

    public static void serializeDischarges(List<Double> dischargeTimes, String directory)
            throws IOException {

        File dir = new File(directory);
        if (!dir.exists()) {
            dir.mkdirs();
        }

        try (FileWriter writer = new FileWriter(directory + "/discharges.txt")) {
            writer.write(dischargeTimes.size() + '\n');

            for (Double t : dischargeTimes) {
                writer.write(String.format("%.5f\n", t));
            }
        }
    }

    public static void serializeSnapshots(
            List<List<Particle>> snapshots, Double dt, String directory) throws IOException {

        // Create directory if it doesn't exist
        File dir = new File(directory);
        if (!dir.exists()) {
            dir.mkdirs();
        }


        try (BufferedWriter writer =
                new BufferedWriter(new FileWriter(directory + "/snapshots.txt"))) {

            int particleCount = snapshots.get(0).size();
            int totalSnapshots = snapshots.size();

            writer.write(particleCount + " " + totalSnapshots + "\n");

            for (int i = 0; i < snapshots.size(); i++) {
                double t = (i + 1) * dt;
                writer.write(String.format("%.5f\n", t));

                List<Particle> particles = snapshots.get(i);
                for (Particle particle : particles) {
                    writer.write(String.format("%.5f %.5f\n", particle.getX(), particle.getY()));
                }
            }
        }
    }
}
