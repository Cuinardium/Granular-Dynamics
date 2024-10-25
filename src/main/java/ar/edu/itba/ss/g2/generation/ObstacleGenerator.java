package ar.edu.itba.ss.g2.generation;

import ar.edu.itba.ss.g2.model.Particle;

import java.util.ArrayList;
import java.util.List;
import java.util.Random;

public class ObstacleGenerator {

    private static final long MAX_TRIES = 1_000_000_000L;

    private final double width;
    private final double length;
    private final int obstacleCount;
    private final double obstacleRadius;


    private final Random random;

    public ObstacleGenerator(
            double width,
            double length,
            int particleCount,
            double particleRadius,
            Random random) {
        this.width = width;
        this.length = length;
        this.obstacleCount = particleCount;
        this.obstacleRadius = particleRadius;
        this.random = random;
    }

    public List<Particle> generate() {
        List<Particle> obstacles = new ArrayList<>(obstacleCount);

        for (int i = 0, tries = 0; i < obstacleCount; i++, tries++) {

            if (tries > MAX_TRIES) {
                throw new IllegalStateException("Could not generate particles without overlaps");
            }

            double x = random.nextDouble() * (length - 2 * obstacleRadius) + obstacleRadius;
            double y = random.nextDouble() * (width - 2 * obstacleRadius) + obstacleRadius;


            Particle particle =
                    new Particle(
                            i,
                            x,
                            0.0,
                            0.0,
                            y,
                            0.0,
                            0.0,
                            0.0,
                            obstacleRadius);

            boolean overlapsObstacle = obstacles.stream().anyMatch(o -> o.overlaps(particle));

            if (overlapsObstacle) {
                i--;
                continue;
            }

            obstacles.add(particle);
        }

        return obstacles;
    }
}
