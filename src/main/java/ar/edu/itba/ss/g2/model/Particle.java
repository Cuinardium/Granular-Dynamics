package ar.edu.itba.ss.g2.model;

public class Particle {
    private int id;

    private Double position;
    private Double velocity;
    private Double acceleration;

    private final Double mass;

    public Particle(int id, Double position, Double v, Double acceleration, Double mass) {
        this.id = id;
        this.position = position;
        this.velocity = v;
        this.acceleration = acceleration;
        this.mass = mass;
    }

    public Particle(Particle particle) {
        this.id = particle.id;
        this.position = particle.position;
        this.velocity = particle.velocity;
        this.acceleration = particle.acceleration;
        this.mass = particle.mass;
    }

    public int getId() {
        return id;
    }

    public Double getPosition() {
        return position;
    }

    public Double getVelocity() {
        return velocity;
    }

    public Double getAcceleration() {
        return acceleration;
    }

    public Double getMass() {
        return mass;
    }

    public void setPosition(Double position) {
        this.position = position;
    }

    public void setVelocity(Double velocity) {
        this.velocity = velocity;
    }

    public void setAcceleration(Double acceleration) {
        this.acceleration = acceleration;
    }

    @Override
    public String toString() {
        return "Particle{"
                + "id="
                + id
                + ", position="
                + position
                + ", v="
                + velocity
                + ", mass="
                + mass
                + '}';
    }

    @Override
    public boolean equals(Object o) {
        if (this == o) return true;
        if (!(o instanceof Particle particle)) return false;
        return this.id == particle.id;
    }

    @Override
    public int hashCode() {
        return Integer.hashCode(id);
    }
}
