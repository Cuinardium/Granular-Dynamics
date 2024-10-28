package ar.edu.itba.ss.g2.simulation;

import ar.edu.itba.ss.g2.model.Particle;
import java.util.ArrayList;
import java.util.List;

public class Simulation {

  private static final int X = 0;
  private static final int Y = 1;

  private final List<Particle> particles;
  private final List<Particle> obstacles;

  private List<Double>[] previousForces;
  private List<Double>[] currentForces;

  private final double width;
  private final double length;
  private final double acceleration;
  private final double normalK;
  private final double tangentialK;
  private final double integrationStep;
  private final double snapshotStep;
  private final double maxTime;

  private double currentTime;

  // ==== Output ===
  private final List<List<Particle>> snapshots;
  private final List<Double> dischargeTimes;

  public Simulation(
      List<Particle> particles,
      List<Particle> obstacles,
      double width,
      double length,
      double acceleration,
      double normalK,
      double tangentialK,
      double integrationStep,
      double snapshotStep,
      double maxTime) {

    this.particles = particles;
    this.obstacles = obstacles;

    int snapshotCount = (int) Math.ceil(maxTime / snapshotStep);
    this.snapshots = new ArrayList<>(snapshotCount);
    this.dischargeTimes = new ArrayList<>();

    this.width = width;
    this.length = length;
    this.acceleration = acceleration;
    this.normalK = normalK;
    this.tangentialK = tangentialK;
    this.integrationStep = integrationStep;
    this.snapshotStep = snapshotStep;
    this.maxTime = maxTime;
  }

  public void run() {
    // Initialize forces
    // TODO: Fuerza anterior
    previousForces = calculateForces();
    currentForces = calculateForces();

    takeSnapshot();

    double currentTime = 0;

    while (currentTime < maxTime) {
      integrate();

      checkDischarges();

      currentTime += integrationStep;

      if (currentTime % snapshotStep == 0) {
        takeSnapshot();
      }
    }
  }

  public List<List<Particle>> getSnapshots() {
    return snapshots;
  }

  public List<Double> getDischargeTimes() {
    return dischargeTimes;
  }

  // ========== Integration =============

  @SuppressWarnings("unchecked")
  private void integrate() {
    List<Double>[] previousVelocities = (List<Double>[]) new List[2];

    previousVelocities[X] = new ArrayList<>(particles.size());
    previousVelocities[Y] = new ArrayList<>(particles.size());

    // Positions
    for (int i = 0; i < particles.size(); i++) {

      Particle particle = particles.get(i);

      double mass = particle.getMass();

      // r(t)
      double currentX = particle.getX();
      double currentY = particle.getY();

      // v(t)
      double currentVx = particle.getVx();
      double currentVy = particle.getVy();

      // a(t)
      double currentAx = currentForces[X].get(i) / mass;
      double currentAy = currentForces[Y].get(i) / mass;

      // a(t-dt)
      double previousAx = previousForces[X].get(i) / mass;
      double previousAy = previousForces[Y].get(i) / mass;

      // r(t+dt)
      double nextX =
          currentX
              + currentVx * integrationStep
              + (2.0 / 3.0) * currentAx * Math.pow(integrationStep, 2)
              - (1.0 / 6.0) * previousAx * Math.pow(integrationStep, 2);

      double nextY =
          currentY
              + currentVy * integrationStep
              + (2.0 / 3.0) * currentAy * Math.pow(integrationStep, 2)
              - (1.0 / 6.0) * previousAy * Math.pow(integrationStep, 2);

      // predicted v(t+dt)
      double predictedVx =
          currentVx
              + (3.0 / 2.0) * currentAx * integrationStep
              - (1.0 / 2.0) * previousAx * integrationStep;

      double predictedVy =
          currentVy
              + (3.0 / 2.0) * currentAy * integrationStep
              - (1.0 / 2.0) * previousAy * integrationStep;

      particle.setX(nextX);
      particle.setY(nextY);
      particle.setVx(predictedVx);
      particle.setVy(predictedVy);
    }

    List<Double>[] nextForces = calculateForces();

    // Correct velocities
    for (int i = 0; i < particles.size(); i++) {

      Particle particle = particles.get(i);

      double mass = particle.getMass();

      // v(t)
      double currentVx = previousVelocities[X].get(i);
      double currentVy = previousVelocities[Y].get(i);

      // a(t-dt), a(t), a(t+dt)
      double previousAx = previousForces[X].get(i) / mass;
      double currentAx = currentForces[X].get(i) / mass;
      double nextAx = nextForces[X].get(i) / mass;

      double previousAy = previousForces[Y].get(i) / mass;
      double currentAy = currentForces[Y].get(i) / mass;
      double nextAy = nextForces[Y].get(i) / mass;

      // corrected v(t+dt)
      double correctedVx =
          currentVx
              + (1.0 / 3.0) * nextAx * integrationStep
              + (5.0 / 6.0) * currentAx * integrationStep
              - (1.0 / 6.0) * previousAx * integrationStep;

      double correctedVy =
          currentVy
              + (1.0 / 3.0) * nextAy * integrationStep
              + (5.0 / 6.0) * currentAy * integrationStep
              - (1.0 / 6.0) * previousAy * integrationStep;

      particle.setVx(correctedVx);
      particle.setVy(correctedVy);
    }

    previousForces = currentForces;

    // Recalculate forces as velocities have changed
    currentForces = calculateForces();
  }
  @SuppressWarnings("unchecked")
  private List<Double>[] calculateForces() {
    List<Double>[] forces = (List<Double>[]) new List[2];
    forces[X] = new ArrayList<>(particles.size());
    forces[Y] = new ArrayList<>(particles.size());

    // Constant acceleration
    for (int i = 0; i < particles.size(); i++) {
      forces[X].add(acceleration);
      forces[Y].add(0.0);
    }

    return forces;
  }

  // ======= Discharges ================

  private void checkDischarges() {
    for (int i = 0; i < particles.size(); i++) {
      Particle particle = particles.get(i);

      // Only in x, if discharged, periodic boundary conditions
      if (particle.getX() < 0) {
        particle.setX(width + particle.getX());
      } else if (particle.getX() > length) {
        particle.setX(particle.getX() - width);
        dischargeTimes.add(currentTime);
      }
    }
  }

  // ======= Snapshots ================

  private void takeSnapshot() {
    snapshots.add(particles.stream().map(Particle::new).toList());
  }
}
