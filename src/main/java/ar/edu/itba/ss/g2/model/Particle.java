package ar.edu.itba.ss.g2.model;

public class Particle implements Comparable<Particle> {
    private int id;

    private Double x;
    private Double vx;
    private Double ax;

    private Double y;

    private final Double mass;
    private final Double radius;

    public Particle(
            int id,
            Double x,
            Double vx,
            Double ax,
            Double y,
            Double vy,
            Double ay,
            Double mass,
            Double radius) {
        this.id = id;
        this.x = x;
        this.vx = vx;
        this.ax = ax;
        this.y = y;
        this.vy = vy;
        this.ay = ay;
        this.mass = mass;
        this.radius = radius;
    }

    public Particle(Particle particle) {
        this.id = particle.id;
        this.x = particle.x;
        this.vx = particle.vx;
        this.ax = particle.ax;
        this.y = particle.y;
        this.vy = particle.vy;
        this.ay = particle.ay;
        this.mass = particle.mass;
        this.radius = particle.radius;
    }

    public int getId() {
        return id;
    }

    public Double getX() {
        return x;
    }

    public Double getVx() {
        return vx;
    }

    public Double getAx() {
        return ax;
    }

    public Double getMass() {
        return mass;
    }

    public void setX(Double x) {
        this.x = x;
    }

    public void setVx(Double vx) {
        this.vx = vx;
    }

    public void setAx(Double ax) {
        this.ax = ax;
    }

    public Double getY() {
        return y;
    }

    public void setY(Double y) {
        this.y = y;
    }

    private Double vy;

    public Double getVy() {
        return vy;
    }

    public void setVy(Double vy) {
        this.vy = vy;
    }

    private Double ay;

    public Double getAy() {
        return ay;
    }

    public void setAy(Double ay) {
        this.ay = ay;
    }

    public Double getRadius() {
        return radius;
    }

    @Override
    public String toString() {
        return "Particle{"
                + "id="
                + id
                + ", x="
                + x
                + ", vx="
                + vx
                + ", ax="
                + ax
                + ", y="
                + y
                + ", vy="
                + vy
                + ", ay="
                + ay
                + ", mass="
                + mass
                + ", radius="
                + radius
                + '}';
    }

    public boolean overlaps(Particle other) {
        double otherX = other.getX();
        double otherY = other.getY();

        double distance = Math.sqrt(Math.pow(x - otherX, 2) + Math.pow(y - otherY, 2));

        return distance < radius + other.getRadius();
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

    @Override
    public int compareTo(Particle other) {
        return Integer.compare(id, other.id);
    }
}
