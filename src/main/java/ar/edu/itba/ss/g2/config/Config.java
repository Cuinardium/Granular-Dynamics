package ar.edu.itba.ss.g2.config;

import java.util.Random;

public class Config {

    // Dimension Entorno
    private final double width; // W
    private final double length; // L

    // Cantidad de particulas
    private final int obstacleCount; // M
    private final int particleCount; // N

    // Tamano particulas
    private final double obstacleRadius; // R
    private final double particleRadius; // r
    private final double particleMass; // m

    // Fuerzas
    private final double acceleration; // A0
    private final double normalK; // k_n
    private final double gamma; // g
    private final double tangentialK; // k_t

    // Tiempos
    private final double integrationStep; // dt
    private final double snapshotStep; // dt2
    private final double maxTime; // tf

    // Output
    private final String outputDirectory; // out
    
    // Seed
    private final long seed;

    public double getWidth() {
        return width;
    }

    public double getLength() {
        return length;
    }

    public int getObstacleCount() {
        return obstacleCount;
    }

    public int getParticleCount() {
        return particleCount;
    }

    public double getObstacleRadius() {
        return obstacleRadius;
    }

    public double getParticleRadius() {
        return particleRadius;
    }

    public double getParticleMass() {
        return particleMass;
    }

    public double getAcceleration() {
        return acceleration;
    }

    public double getNormalK() {
        return normalK;
    }

    public double getGamma() {
        return gamma;
    }

    public double getTangentialK() {
        return tangentialK;
    }

    public double getIntegrationStep() {
        return integrationStep;
    }

    public double getSnapshotStep() {
        return snapshotStep;
    }

    public double getMaxTime() {
        return maxTime;
    }

    public String getOutputDirectory() {
        return outputDirectory;
    }

    public long getSeed() {
        return seed;
    }

    private Config(Builder builder) {
        this.width = builder.width;
        this.length = builder.length;
        this.obstacleCount = builder.obstacleCount;
        this.particleCount = builder.particleCount;
        this.obstacleRadius = builder.obstacleRadius;
        this.particleRadius = builder.particleRadius;
        this.particleMass = builder.particleMass;
        this.acceleration = builder.acceleration;
        this.normalK = builder.normalK;
        this.gamma = builder.gamma;
        this.tangentialK = builder.tangentialK;
        this.integrationStep = builder.integrationStep;
        this.snapshotStep = builder.snapshotStep;
        this.maxTime = builder.maxTime;
        this.outputDirectory = builder.outputDirectory;
        this.seed = builder.seed;
    }

    public static class Builder {
        private double width;
        private double length;
        private int obstacleCount;
        private int particleCount;
        private double obstacleRadius;
        private double particleRadius;
        private double particleMass;
        private double acceleration;
        private double normalK;
        private double gamma;
        private double tangentialK;
        private double integrationStep;
        private double snapshotStep;
        private double maxTime;
        private String outputDirectory;

        private long seed = System.currentTimeMillis(); 

        public Builder width(double width) {
            this.width = width;
            return this;
        }

        public Builder length(double length) {
            this.length = length;
            return this;
        }

        public Builder obstacleCount(int obstacleCount) {
            this.obstacleCount = obstacleCount;
            return this;
        }

        public Builder particleCount(int particleCount) {
            this.particleCount = particleCount;
            return this;
        }

        public Builder obstacleRadius(double obstacleRadius) {
            this.obstacleRadius = obstacleRadius;
            return this;
        }

        public Builder particleRadius(double particleRadius) {
            this.particleRadius = particleRadius;
            return this;
        }

        public Builder particleMass(double particleMass) {
            this.particleMass = particleMass;
            return this;
        }

        public Builder acceleration(double acceleration) {
            this.acceleration = acceleration;
            return this;
        }

        public Builder normalK(double normalK) {
            this.normalK = normalK;
            return this;
        }

        public Builder gamma(double gamma) {
            this.gamma = gamma;
            return this;
        }

        public Builder tangentialK(double tangentialK) {
            this.tangentialK = tangentialK;
            return this;
        }

        public Builder integrationStep(double integrationStep) {
            this.integrationStep = integrationStep;
            return this;
        }

        public Builder snapshotStep(double snapshotStep) {
            this.snapshotStep = snapshotStep;
            return this;
        }

        public Builder maxTime(double maxTime) {
            this.maxTime = maxTime;
            return this;
        }

        public Builder outputDirectory(String outputDirectory) {
            this.outputDirectory = outputDirectory;
            return this;
        }

        public Builder seed(long seed) {
            this.seed = seed;
            return this;
        }

        public Config build() {
            return new Config(this);
        }
    }
}
