package ar.edu.itba.ss.g2.generation;

import ar.edu.itba.ss.g2.model.Particle;

import java.util.ArrayList;
import java.util.List;
import java.util.Random;

public class ParticleGenerator {

    private static final long MAX_TRIES = 1_000_000_000L;

    private final double width;
    private final double length;
    private final int particleCount;
    private final double particleRadius;
    private final double particleMass;
    private final double initialAcceleration;

    private final List<Particle> obstacles;

    private final Random random;

    public ParticleGenerator(
            double width,
            double length,
            int particleCount,
            double particleRadius,
            double particleMass,
            double initialAcceleration,
            List<Particle> obstacles,
            Random random) {
        this.width = width;
        this.length = length;
        this.particleCount = particleCount;
        this.particleRadius = particleRadius;
        this.particleMass = particleMass;
        this.initialAcceleration = initialAcceleration;
        this.obstacles = obstacles;
        this.random = random;
    }

    public List<Particle> generate() {
        List<Particle> particles = new ArrayList<>(particleCount);

        for (int i = 0, tries = 0; i < particleCount; i++, tries++) {

            if (tries > MAX_TRIES) {
                throw new IllegalStateException("Could not generate particles without overlaps");
            }

            double x = random.nextDouble() * (length - 2 * particleRadius) + particleRadius;
            double y = random.nextDouble() * (width - 2 * particleRadius) + particleRadius;

            double ax = initialAcceleration;

            Particle particle =
                    new Particle(
                            i,
                            x,
                            0.0,
                            ax,
                            y,
                            0.0,
                            0.0,
                            particleMass,
                            particleRadius);

            boolean overlapsParticle = particles.stream().anyMatch(p -> p.overlaps(particle));
            boolean overlapsObstacle = obstacles.stream().anyMatch(o -> o.overlaps(particle));

            if (overlapsObstacle || overlapsParticle) {
                i--;
                continue;
            }

            particles.add(particle);
        }

        return particles;
    }
}
